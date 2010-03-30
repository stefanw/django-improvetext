import datetime
import pickle
from difflib import SequenceMatcher, Differ, restore

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.html import escape

from bundestagger.account.models import User

class ImprovementManager(models.Manager):
    def suggest(self, obj=None, field="", change="", user=None):
        obj_type = ContentType.objects.get_for_model(obj)
        d = Differ()
        original = getattr(obj,field).encode("utf8").splitlines(True)
        change = unicode(change).encode("utf8").splitlines(True)
        difflist = list(d.compare(original,change))
        diff = pickle.dumps(difflist).encode("utf8")
#        diff = diff.decode("utf8")
        return self.create(user=user,content_type=obj_type,object_id=obj.id,field=field,diff=diff)

class Improvement(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    diff = models.TextField(blank=True)
    applied = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    objects = ImprovementManager()
    
    def __unicode__(self):
        return u"Improvement on %s (%s) by %s" % (unicode(self.content_object), self.field, self.user)
        
    def get_absolute_url(self):
        return u"/bundesadmin/improvetext/improvement/%d/" % (self.id)

    @property    
    def change(self):
        return "".join(list(restore(pickle.loads(self.diff.encode("utf8")),2)))
        
    @property    
    def original(self):
        return "".join(list(restore(pickle.loads(self.diff.encode("utf8")),1)))
                
    def revert(self):
        assert self.applied
        setattr(self.content_object,self.field, self.original)
        self.content_object.save()
        if hasattr(self.content_object, "clear_cache"):
            self.content_object.clear_cache()
        self.applied = False
        self.save()
        
    def apply(self):
        if self.field == "id" and self.change == "None":
            self.content_object.delete()
        else:
            setattr(self.content_object,self.field, self.change)
            self.content_object.save()
            if hasattr(self.content_object, "clear_cache"):
                self.content_object.clear_cache()
        self.applied=True
        self.save()
            
    def get_html_diff(self):
        old_text = escape(self.original)
        new_text = escape(self.change)
        old_offset = 0
        new_offset = 0
        s = SequenceMatcher(None, old_text, new_text)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == "delete" or tag == "replace":
                old_text = old_text[:i1+old_offset]+"<del>"+old_text[i1+old_offset:i2+old_offset]+"</del>"+old_text[i2+old_offset:]
                old_offset += len("<del></del>")
            if tag == "insert" or tag == "replace":
                new_text = new_text[:j1+new_offset]+"<ins>"+new_text[j1+new_offset:j2+new_offset]+"</ins>"+new_text[j2+new_offset:]
                new_offset += len("<ins></ins>")
        return (old_text, new_text)

