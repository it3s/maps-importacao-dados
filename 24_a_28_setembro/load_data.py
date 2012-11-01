# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodecsv
from datetime import datetime

from authentication.models import User
from organization.models import (Organization, OrganizationCategoryTranslation,
        OrganizationBranch)
from need.models import TargetAudience
from komoo_resource.models import Resource
from komoo_project.models import Project, ProjectRelatedObject
from django.contrib.contenttypes.models import ContentType


ct_resource = ContentType.objects.get_for_model(Resource)
ct_organization = ContentType.objects.get_for_model(Organization)

# build field index
alpha = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
field_index = alpha[:]
for pre in ['A', 'B']:
    for b in alpha:
        if (pre + b) == 'BR':
            break
        else:
            field_index.append(pre + b)
field_index = {k: i for i, k in enumerate(field_index)}


def get_field(vals, field):
    return vals[field_index[field]]

count = 0


def format_fields(vals, *args):
    fmt = {}
    for arg in args:
        fmt[arg] = get_field(vals, arg)
    return fmt


def save_org(vals):
    e = get_field(vals, 'E').title().strip()
    d = get_field(vals, 'D').strip()

    if d:
        name = '{} - {}'.format(e, d)
    else:
        name = e

    if not name:
        return

    distrito = get_field(vals, 'M').strip()
    if distrito:
        desc = """
#### Localização

{C} fica {M} {N}, {O} do município {Q}, {R}.
""".format(**format_fields(vals, 'C', 'M', 'N', 'O', 'Q', 'R'))
    else:
        desc = """
#### Localização

{C} fica no bairro {L} do município {Q}, {R}.
""".format(**format_fields(vals, 'C', 'L', 'Q', 'R'))
    desc += """

#### Serviços e Programas

{AM} {AN}

#### Funcionamento

* Horário: {BG}
* Situação: {BJ}

#### Área de abrangência

{BF}

#### Registros e certificações

""".format(**format_fields(vals, 'AM', 'AN', 'BG', 'BJ', 'BF'))

    g = get_field(vals, 'G')
    bm = get_field(vals, 'BM')
    h = get_field(vals, 'H')
    bh = get_field(vals, 'BH')
    z = get_field(vals, 'Z')

    if g:
        desc += """
- Código da Escola (INEP): {G}
""".format(G=g)

    if bm:
        desc += """
- Código Municipal da Escola: {BM}
""".format(BM=bm)

    if h:
        desc += """
- Cadastro Nacional de Estabelecimentos de Saúde (CNES): {H}
""".format(H=h)

    if bh:
        desc += """
- Código do Conselho Tutelar: {BH}
""".format(BH=bh)

    if z:
        desc += """
- CNPJ: {Z}
""".format(Z=z)

    desc += """
#### Órgão superior

- {BO}

#### Pessoas de contato

{W}, {X}

#### Outros contatos

Fax: ({S}) {U}

#### Referências

- [{AE}]({AF} "{AG}"), consultado em {AH}
""".format(**format_fields(vals, 'BO', 'W', 'X', 'S', 'U', 'AE', 'AF', 'AG',
           'AH'))

    k = get_field(vals, 'K').strip()
    if k:
        k = ', ' + k

    contact = """
Endereço: {I}, {J} {K} | {L}, {P} | {Q}-{R}

Telefone: ({S}) {T}

E-mail: {V}
    """.format(K=k, **format_fields(vals, 'I', 'J', 'L', 'P', 'Q', 'R', 'S',
                'T', 'V'))

    link = get_field(vals, 'Y')

    tags = [get_field(vals, f) for f in
               ['AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX',
                'BN', 'BO', 'BP', 'BQ']]
    tags = filter(bool, tags)

    # Público-Alvo
    public = [get_field(vals, f) for f in ['AY', 'AZ', 'BA', 'BB', 'BC', 'BD']]
    public = filter(bool, public)

    now = datetime.now()
    user_id = get_field(vals, 'B').split('/')[-1]
    creator = User.objects.get(pk=user_id)

    categories = [get_field(vals, column) for column in
                        ['AA', 'AB', 'AC', 'AD']]
    categories = filter(bool, categories)

    categorias = []
    for cat in categories:
        c = OrganizationCategoryTranslation.objects.filter(name__icontains=cat)
        if c.count():
            categorias.append(c[0].category)

    longitude, latitude = get_field(vals, 'BL'), get_field(vals, 'BK')
    if longitude and latitude:
        x, y = map(float, [c.replace(',', '.').replace(' ', '')
                    for c in (longitude, latitude)])
        geom = []
        geom.append('%s,%s' % (x + 0.0005, y + 0.0005))
        geom.append('%s,%s' % (x + 0.0005, y - 0.0005))
        geom.append('%s,%s' % (x - 0.0005, y - 0.0005))
        geom.append('%s,%s' % (x - 0.0005, y + 0.0005))
        geom.append('%s,%s' % (x + 0.0005, y + 0.0005))
        coords = ''
        for i, coord in enumerate(geom):
            coord = coord.split(',')
            coords += '%s %s' % (coord[1], coord[0])
            if not i == len(geom) - 1:
                coords += ', '
        geometry = "GEOMETRYCOLLECTION( POLYGON (( %s )))" % coords
    else:
        geometry = ''

    o = Organization()
    while Organization.objects.filter(name=name).count():
        name += ' '
    o.name = name
    o.description = desc
    o.contact = contact
    o.link = link
    o.category = categorias
    o.creation_date = now
    o.creator = creator
    o.save()
    if geometry:
        OrganizationBranch.objects.create(name='sede', geometry=geometry,
                organization=o)
    for t in tags:
        o.tags.add(t)
    for p in public:
        p, c = TargetAudience.objects.get_or_create(name=p)
        o.target_audiences.add(p)

    proj_slug = get_field(vals, 'BE').split('/')[-1]
    if proj_slug:
        proj = Project.objects.get(slug=proj_slug)
        ProjectRelatedObject.objects.get_or_create(project=proj,
                content_type=ct_organization, object_id=o.id)

    print 'OK  -  ', name


def save_resource(vals):
    e = get_field(vals, 'E').title().strip()
    d = get_field(vals, 'D').strip()

    if d:
        name = '{} - {}'.format(e, d)
    else:
        name = e

    if not name:
        return

    distrito = get_field(vals, 'M').strip()
    if distrito:
        desc = """
#### Localização

{C} fica {M} {N}, {O} do município {Q}, {R}.
""".format(**format_fields(vals, 'C', 'M', 'N', 'O', 'Q', 'R'))
    else:
        desc = """
#### Localização

{C} fica no bairro {L} do município {Q}, {R}.
""".format(**format_fields(vals, 'C', 'L', 'Q', 'R'))
    desc += """

#### Serviços e Programas

{AM} {AN}

#### Funcionamento

* Horário: {BG}
* Situação: {BJ}

#### Área de abrangência

{BF}

#### Registros e certificações

""".format(**format_fields(vals, 'AM', 'AN', 'BG', 'BJ', 'BF'))

    g = get_field(vals, 'G')
    bm = get_field(vals, 'BM')
    h = get_field(vals, 'H')
    bh = get_field(vals, 'BH')
    z = get_field(vals, 'Z')

    if g:
        desc += """
- Código da Escola (INEP): {G}
""".format(G=g)

    if bm:
        desc += """
- Código Municipal da Escola: {BM}
""".format(BM=bm)

    if h:
        desc += """
- Cadastro Nacional de Estabelecimentos de Saúde (CNES): {H}
""".format(H=h)

    if bh:
        desc += """
- Código do Conselho Tutelar: {BH}
""".format(BH=bh)

    if z:
        desc += """
- CNPJ: {Z}
""".format(Z=z)

    desc += """
#### Órgão superior

- {BO}

#### Pessoas de contato

{W}, {X}

#### Outros contatos

Fax: ({S}) {U}

#### Referências

- [{AE}]({AF} "{AG}"), consultado em {AH}
""".format(**format_fields(vals, 'BO', 'W', 'X', 'S', 'U', 'AE', 'AF', 'AG',
           'AH'))

    k = get_field(vals, 'K').strip()
    if k:
        k = ', ' + k

    contact = """
Endereço: {I}, {J} {K} | {L}, {P} | {Q}-{R}

Telefone: ({S}) {T}

E-mail: {V}
    """.format(K=k, **format_fields(vals, 'I', 'J', 'L', 'P', 'Q', 'R', 'S',
                'T', 'V'))

    tags = [get_field(vals, f) for f in
               ['AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX',
                'BN', 'BO', 'BP', 'BQ']]
    tags = filter(bool, tags)

    now = datetime.now()
    user_id = get_field(vals, 'B').split('/')[-1]
    creator = User.objects.get(pk=user_id)

    longitude, latitude = get_field(vals, 'BL'), get_field(vals, 'BK')
    if longitude and latitude:
        x, y = map(float, [c.replace(',', '.').replace(' ', '')
                    for c in (longitude, latitude)])
        geom = []
        geom.append('%s,%s' % (x + 0.0005, y + 0.0005))
        geom.append('%s,%s' % (x + 0.0005, y - 0.0005))
        geom.append('%s,%s' % (x - 0.0005, y - 0.0005))
        geom.append('%s,%s' % (x - 0.0005, y + 0.0005))
        geom.append('%s,%s' % (x + 0.0005, y + 0.0005))
        coords = ''
        for i, coord in enumerate(geom):
            coord = coord.split(',')
            coords += '%s %s' % (coord[1], coord[0])
            if not i == len(geom) - 1:
                coords += ', '
        geometry = "GEOMETRYCOLLECTION( POLYGON (( %s )))" % coords
    else:
        geometry = ''

    o = Resource()
    o.name = name
    o.description = desc
    o.contact = contact
    o.creation_date = now
    o.creator = creator
    if geometry:
        o.geometry = geometry
    o.save()
    for t in tags:
        o.tags.add(t)

    proj_slug = get_field(vals, 'BE').split('/')[-1]
    if proj_slug:
        print proj_slug
        proj = Project.objects.get(slug=proj_slug)
        ProjectRelatedObject.objects.get_or_create(project=proj,
                content_type=ct_resource, object_id=o.id)

    print 'OK  -  ', name


def save_obj(vals):
    global count
    if get_field(vals, 'F') == 'sim':
        if get_field(vals, 'A') == 'R':
            save_resource(vals)
        elif get_field(vals, 'A') == 'O':
            save_org(vals)
        count += 1

fname = 'importation/dados.csv'
rows = unicodecsv.reader(open(fname), encoding='utf-8')

for row in rows:
    save_obj(row)

print 'count: ', count


