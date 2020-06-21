#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_login import UserMixin

from .. import db
from ..helpers import CoreMixin


class User(CoreMixin, db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    msisdn = db.Column(db.String(16))

    def __unicode__(self):
        return str(self.id) or ""

    def to_json(self):
        params = {}
        if self.first_name is not None:
            params["first_name"] = self.first_name
        if self.last_name is not None:
            params["last_name"] = self.last_name
        if self.msisdn is not None:
            params["msisdn"] = self.msisdn
        params["id"] = self.id
        return params
