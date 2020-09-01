# django-content-subscriptions ![Travis (.com) branch](https://img.shields.io/travis/com/e-dang/django-content-subscriptions/master?label=master) ![Travis (.com) branch](https://img.shields.io/travis/com/e-dang/django-content-subscriptions/dev?label=dev)

## Description

This is a pluggable django application that enables instances of a model to subscribe (i.e. read, but not write) to generic types of content owned by other instances of the same model.

For example, given the models User and Item where a single User can own multiple Items (ForeignKey on Item to User), this app allows specific User instances to subscribe to another User instance's Items, thus allowing those items to be seen by the subscribing User. More concretely, given two Users, u1 and u2, where u1 owns Items i1, i2 and u2 owns Items i3, i4, then u1 can subscribe to u2's Items, thus allowing u1 to read i1, i2, i3, i4, but only write to i1 and i2. Conversley, u2 is only able to read/write i3 and i4. This sort of functionality can be applied to any combination of models that have the same type of relationship as Item.

This app also allows for fine-grained control over which content instances are shared and shown to each user through a subscription. From the above example, u1 could choose to hide i3 from their list of Items, and thus only see i1, i2, i4. Conversley, u2 could choose to hide i3, in which case u1 would only ever be able to see i1, i2, i4 unless u2 decided to reshare i3.