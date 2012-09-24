#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ========= environment config ====== ##
from __future__ import unicode_literals
import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
PROJ_DIR = os.path.abspath(os.path.join(HERE, '../..'))
SITE_ROOT = os.path.abspath(os.path.join(PROJ_DIR, '../..'))

env_ = os.environ.get('KOMOO_ENV', 'dev')

sys.path.append(PROJ_DIR)
sys.path.append(SITE_ROOT)

from django.core.management import setup_environ

env_name = ['', 'development', 'staging', 'production'][
            3 * (int(env_ == 'prod')) +
            2 * (int(env_ == 'stage')) +
                (int(env_ == 'dev'))]
environ = None
exec 'from settings import {} as environ'.format(env_name)
setup_environ(environ)

## ======= script ====== ##
import unicodecsv
from django.contrib.auth.models import User
from datetime import datetime
from organization.models import OrganizationCategoryTranslation, Organization
from need.models import TargetAudience
from komoo_resource.models import Resource

mariarita = User.objects.get(username='mariarita')

# build field index
alpha = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
field_index = alpha[:]
for b in alpha:
    if ('A' + b) == 'AQ':
        break
    else:
        field_index.append('A' + b)
field_index = {k: i for i, k in enumerate(field_index)}


def get_field(vals, field):
    return vals[field_index[field]]

count = 0


def save_org(vals):
    name = "{} {}".format(
            get_field(vals, 'D'), get_field(vals, 'E'))

    desc = """
####Localização

{C} fica no distrito {K} da Subprefeitura {L} da capital paulista.

####Horário de Atendimento

{Y}

""".format(
        C=get_field(vals, 'C'),
        K=get_field(vals, 'K'),
        L=get_field(vals, 'L'),
        Y=get_field(vals, 'Y'),
    )

    if get_field(vals, 'G') or get_field(vals, 'S'):
        desc += """
####Registros e Certificações

"""
        if get_field(vals, 'G'):
            desc += """
- Código INEP da Instituição de Ensino: {G}""".format(G=get_field(vals, 'G'))
        if get_field(vals, 'S'):
            desc += """
- Cadastro Nacional de Pessoa Jurídica (CNPJ): {S}""".format(S=get_field(
                                                                vals, 'S'))

    desc += """

####Referência

- [{U}]({V} "{W}"), {X}
    """.format(
        U=get_field(vals, 'U'),
        V=get_field(vals, 'V'),
        W=get_field(vals, 'W'),
        X=get_field(vals, 'X'),
    )

    contact = """
{H}, {I} | {J}
CEP: {M}, São Paulo-SP

Fone: {O} {P}

Email: {Q}
    """.format(
        H=get_field(vals, 'H'),
        I=get_field(vals, 'I'),
        J=get_field(vals, 'J'),
        M=get_field(vals, 'M'),
        O=get_field(vals, 'O'),
        P=get_field(vals, 'P'),
        Q=get_field(vals, 'Q'),
    )

    link = get_field(vals, 'R')

    cat = get_field(vals, 'T')
    if cat == 'Cultura': cat = 'Cultura e Arte'
    categoria = ''
    if cat:
        cat = OrganizationCategoryTranslation.objects.filter(name__icontains=cat)
        if cat.count():
            categoria =cat[0].category


    # Palavras-Chave
    tags = [get_field(vals, f) for f in [ 'Z', 'AA', 'AB', 'AC', 'AD', 'AE'] ]

    # Público-Alvo
    public = [get_field(vals, f) for f in [
        'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP']]

    now = datetime.now()

    o = Organization()
    o.name = name
    o.description = desc
    o.contact = contact
    o.link = link
    o.category = categoria
    o.creation_date = now
    o.creator = mariarita
    o.save()
    for t in tags:
        o.tags.add(t)
    for p in public:
        p, c = TargetAudience.objects.get_or_create(name=p)
        o.target_audiences.add(p)
    print 'OK'

def save_resource(vals):
    name = "{} {}".format(
            get_field(vals, 'D'), get_field(vals, 'E'))

    desc = """
####Localização

{C} fica no distrito {K} da Subprefeitura {L} da capital paulista.

####Horário de Atendimento

{Y}

""".format(
        C=get_field(vals, 'C'),
        K=get_field(vals, 'K'),
        L=get_field(vals, 'L'),
        Y=get_field(vals, 'Y'),
    )

    if get_field(vals, 'G') or get_field(vals, 'S'):
        desc += """
####Registros e Certificações

"""
        if get_field(vals, 'G'):
            desc += """
- Código INEP da Instituição de Ensino: {G}""".format(G=get_field(vals, 'G'))
        if get_field(vals, 'S'):
            desc += """
- Cadastro Nacional de Pessoa Jurídica (CNPJ): {S}""".format(S=get_field(
                                                                vals, 'S'))

    desc += """

####Referência

- [{U}]({V} "{W}"), {X}
    """.format(
        U=get_field(vals, 'U'),
        V=get_field(vals, 'V'),
        W=get_field(vals, 'W'),
        X=get_field(vals, 'X'),
    )

    contact = """
{H}, {I} | {J}
CEP: {M}, São Paulo-SP

Fone: {O} {P}

Email: {Q}
    """.format(
        H=get_field(vals, 'H'),
        I=get_field(vals, 'I'),
        J=get_field(vals, 'J'),
        M=get_field(vals, 'M'),
        O=get_field(vals, 'O'),
        P=get_field(vals, 'P'),
        Q=get_field(vals, 'Q'),
    )


    # Palavras-Chave
    tags = [get_field(vals, f) for f in [ 'Z', 'AA', 'AB', 'AC', 'AD', 'AE'] ]

    now = datetime.now()

    o = Resource()
    o.name = name
    o.description = desc
    o.contact = contact
    o.creation_date = now
    o.creator = mariarita
    o.save()
    for t in tags:
        o.tags.add(t)
    print 'OK'


def save_obj(vals):
    global count
    if get_field(vals, 'F') == 'sim':
        if get_field(vals, 'A') == 'R':
            save_resource(vals)
        elif get_field(vals, 'A') == 'O':
            save_org(vals)
        count += 1

fname = 'scripts/cenpec/cenpec.csv'
rows = unicodecsv.reader(open(fname), encoding='utf-8')

for row in rows:
    save_obj(row)

print 'count: ', count

