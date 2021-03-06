from datetime import datetime

from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.sites.models import Site

from django.conf import settings

GUESTBOOK_ENTRY_MAX_LENGTH = getattr(settings,'GUESTBOOK_ENTRY_MAX_LENGTH', 3000)

class Entry(models.Model):


    site        = models.ForeignKey(Site)

    submit_date = models.DateTimeField(_('date'), default=datetime.now(), blank=True)
    ip          = models.IPAddressField(_('IP address'), blank=True, null=True)
    user        = models.CharField(_('user'), max_length=200)
    email       = models.EmailField(_('e-mail'), blank=True, null=True)
    url         = models.URLField(_('website'), blank=True, null=True)

    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    text = models.TextField(_('Message'), max_length=GUESTBOOK_ENTRY_MAX_LENGTH)
    
    class Meta:
        ordering = ['-submit_date','user']
        
    def __unicode__(self):
        return _("%(user)s on %(date)s") % {'user' : self.user, 
                                            'date' : self.submit_date}
    
    def get_replies(self):
    	replies=[]
    	replies=self.replies.all()
    	return replies
    
    def save(self, force_insert=False, force_update=False):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(Entry, self).save(force_insert, force_update)

class Reply(models.Model):
    entry       = models.ForeignKey(Entry,related_name='replies')
    user        = models.CharField(_('user'), max_length=200)
    submit_date = models.DateTimeField(_('date'), default=datetime.now(), blank=True)
    ip          = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))
    text = models.TextField(_('Reply'), max_length=255)
    
    class Meta:
        ordering = ['-submit_date','user']

    def __unicode__(self):
        return _("%(user)s on %(date)s") % {'user' : self.user, 
                                            'date' : self.submit_date}
    
    def save(self, force_insert=False, force_update=False):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(Reply, self).save(force_insert, force_update)