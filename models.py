import re
import feedparser
import orm as model

class User(model.Model):
    username = model.Field()
    default_user = model.Field(default=False)
    unread_only = model.Field(default=False) 

    def subscribed(self):
        feeds = []
        for sub in Subscription.all(user=self):
            feeds.append(Feed.get(id=sub.feed.id))
        return feeds 

    def set_default_user(self):
        u = User.get(default_user=True)
        u.default_user = False
        u.save()
        self.default_user = True
        self.save()

    @classmethod
    def get_default_user(self):
        return User.get(default_user=True)


class Feed(model.Model):
    user = model.ForeignKey(User)
    title = model.Field()
    link = model.Field()
#    subscribed = model.Field(default=True)
    rss = model.Field()

    def get_feed(self):
        feed = feedparser.parse(self.rss)
        return feed

    @classmethod
    def feed_exists(cls, link):
        return not Feed.is_unique(link=link)

class Subscription(model.Model):
    feed = model.ForeignKey(Feed)
    user = model.ForeignKey(User)

class FeedList(model.Model):
    name = model.Field()
    user = model.ForeignKey(User)

    @classmethod
    def check_unique(cls, user, name):
        return FeedList.is_unique(user=user, name=name)

class FeedListItem(model.Model):
    feed_list = model.ForeignKey(FeedList)
    feed = model.ForeignKey(Feed)

    @classmethod
    def get_feeds(cls, feed_list):
        feeds = []
        for i in FeedListItem.all(feed_list=feed_list):
            feeds.append(i.feed)
        return feeds

class Entry(model.Model):
    feed = model.ForeignKey(Feed)
    user = model.ForeignKey(User)
    starred = model.Field(default=False)
    title = model.Field()
    updated = model.Field()
    created = model.Field()
    author = model.Field()
    content = model.Field()
    link = model.Field()

    def set_source(self):
        source_sub = re.sub('https?://', '', self.link)
        source = source_sub.split('/')[0]
        source = source.split('.')
        source = '.'.join(source[-2:])
        self.source = source

    def get_source(self):
        self.set_source()
        return self.source

    @classmethod
    def entry_exists(cls, link):
        return not Entry.is_unique(link=link)

    @classmethod
    def get_starred(cls, user):
        return list(Entry.all(user=user, starred=True))

    @classmethod
    def search_all(cls, user, query):
        matches = []
        for e in Entry.all(user=user):
            if query in e.title.lower() or query in c.content.lower():
                matches.append(e)
        return matches

class EntryList(model.Model):
    name = model.Field()
    user = model.ForeignKey(User)

class EntryListItem(model.Model):
    entry_list = model.ForeignKey(EntryList)
    entry = model.ForeignKey(Entry)

    @classmethod
    def get_articles(cls, entry_list):
        articles = []
        for i in EntryListItem.all(entry_list=entry_list):
            articles.append(Entry.get(id=i.id))
        return articles

class Filter(model.Model):
    name = model.Field()
    user = model.ForeignKey(User)

class FilterItem(model.Model):
    filter = model.ForeignKey(Filter)
    entry = model.ForeignKey(Entry)

    @classmethod
    def get_articles(cls, filter_, limit='ALL', offset=0):
        entries = []
        for item in FilterItem.all(separator='OR', order_by='-id', limit=limit, offset=offset, filter=filter_):
            entries.append(Entry.get(id=item.entry.id))
        return entries 
