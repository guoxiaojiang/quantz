from unittest import TestCase

import mongoengine as mongo
from mongoengine import *
import datetime


class SubModel(Document):
    group_key = StringField(required=True)
    title = StringField(required=True)
    price = FloatField(required=True)


class GroupKey(Document):
    the_key = StringField(required=True)


class SomeModel(Document):
    foreignKey = StringField()
    when = DateTimeField()
    subModel = ListField(ReferenceField(SubModel))


class MongodbTest(TestCase):
    def setUp(self) -> None:
        mongo.connect('quant_test', host='localhost', port=27017)

    def test_mongodb(self):
        SubModel.objects().delete()
        SomeModel.objects().delete()
        sub1 = SubModel(group_key='xxxx', title='SUB1', price=11.22).save()
        sub2 = SubModel(group_key='zzzzz', title='SUB2', price=33.44).save()
        SomeModel(when=datetime.datetime.today(), subModel=[sub1, sub2]).save()
        SomeModel(when=datetime.datetime.today(), subModel=[sub2, sub1]).save()
        print(SomeModel.objects())
        for model in SomeModel.objects():
            print(model.when)
            for sub in model.subModel:
                print('%s %s %s' % (sub.group_key, sub.title, sub.price))

    def test_foreign_key(self):
        """
        这个方法简单，项目中暂时采用此方案，如有更好的方案，再优化
        :return:
        """
        GroupKey.objects().delete()
        SubModel.objects().delete()
        day1_key = datetime.datetime(year=2019, month=1, day=1)
        day2_key = datetime.datetime(year=2019, month=4, day=10)
        key1 = GroupKey(the_key=str(day1_key))
        key2 = GroupKey(the_key=str(day2_key))
        key1.save()
        key2.save()
        sub1_1 = SubModel(group_key=str(day1_key), title='sub1_1', price=11.11)
        sub1_2 = SubModel(group_key=str(day1_key), title='sub1_2', price=22.22)
        sub1_1.save()
        sub1_2.save()
        sub2_1 = SubModel(group_key=str(day2_key),
                          title='sub2_1', price=33311.11)
        sub2_2 = SubModel(group_key=str(day2_key),
                          title='sub2_2', price=444422.22)
        sub2_1.save()
        sub2_2.save()
        for key in GroupKey.objects():
            print('%s' % key.the_key)
            subs = SubModel.objects(group_key=key.the_key)
            for sub in subs:
                print('%s %s %s' % (sub.group_key, sub.title, sub.price))

    def tearDown(self) -> None:
        pass
