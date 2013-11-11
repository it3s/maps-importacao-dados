# -*- coding: utf-8 -*-
from datetime import *
from authentication.models import User
from komoo_project.models import Project
from update.models import Update

def get_project_creators():
    creators = set([proj.creator for proj in Project.objects.all() if proj.creator])
    for u in creators:
        print "id: %s  name: %s  email: %s " % (u.id, u.name, u.email)

def find_most_active():
    users = []
    for u in User.objects.all():
        users.append({
            "score": sum([ u.created_communities.count(),
                        u.created_investments.count(),
                        u.created_projects.count(),
                        u.created_georefobject.count(),
                        u.created_needs.count(),
                        u.created_proposals.count(),
                        u.created_importsheets.count(),
                        u.created_organizations.count(),
                        u.created_resources.count()]),
            "id": u.id,
            "email": u.email,
            "name": u.name,
        })
    most_active = sorted(users, key=lambda usr: usr["score"])[:-31:-1]
    for u in most_active:
        print "id: %s  name: %s  email: %s  score: %s" % (u["id"], u["name"], u["email"], u["score"])


def active_latelly():
    threshould_date = datetime.now() - timedelta(days=90)
    updates = Update.objects.filter(date__gt=threshould_date)
    user_ids = set()
    for upd in updates:
        user_ids |= set([u['id'] for u in upd.users])

    for u in [User.objects.get(pk=id) for id in user_ids]:
        print "id: %s  name: %s  email: %s " % (u.id, u.name, u.email)
