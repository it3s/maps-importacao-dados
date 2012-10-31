# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodecsv
from datetime import datetime


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
""".format(**format_fields(vals, 'C','M','N','O','Q', 'R'))
    else:
        desc = """
#### Localização

{C} fica no bairro {L} do município {Q}, {R}.
""".format(**format_fields(vals, 'C','L','Q','R'))
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
""".format(G=get_field(vals, 'G'))

    if bm:
        desc += """
- Código Municipal da Escola: {BM}
""".format(G=get_field(vals, 'BM'))

    if h:
        desc += """
- Cadastro Nacional de Estabelecimentos de Saúde (CNES): {H}
""".format(H=get_field(vals, 'H'))

    if bh:
        desc += """
- Código do Conselho Tutelar: {BH}
""".format(BH=get_field(vals, 'BH'))

    if z:
        desc += """
- CNPJ: {Z}
""".format(Z=get_field(vals, 'Z'))

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

    contact = """
Endereço: {I}, {J} {K} | {L}, {P} | {Q}-{R}

Telefone: ({S}) {T}

E-mail: {V}
    """.format(K=k, **format_fields(vals, 'I', 'J', 'L', 'P', 'Q', 'R', 'S',
                'T', 'V'))

    link = get_field(vals, 'Y')

    tags = [get_field(vals, f) for f in
            ['AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW']]

    # Público-Alvo
    public = [get_field(vals, f) for f in ['AM', 'AN', 'AO', 'AP']]

    now = datetime.now()

    o = Organization()
    o.name = name
    o.description = desc
    o.contact = contact
    o.link = link
    # o.category = categoria
    # o.creation_date = now
    # o.creator = users[get_field(vals, 'C')]
    # o.save()
    # for t in tags:
    #     o.tags.add(t)
    # for p in public:
    #     p, c = TargetAudience.objects.get_or_create(name=p)
    #     o.target_audiences.add(p)

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
""".format(**format_fields(vals, 'C','M','N','O','Q', 'R'))
    else:
        desc = """
#### Localização

{C} fica no bairro {L} do município {Q}, {R}.
""".format(**format_fields(vals, 'C','L','Q','R'))
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
""".format(G=get_field(vals, 'G'))

    if bm:
        desc += """
- Código Municipal da Escola: {BM}
""".format(G=get_field(vals, 'BM'))

    if h:
        desc += """
- Cadastro Nacional de Estabelecimentos de Saúde (CNES): {H}
""".format(H=get_field(vals, 'H'))

    if bh:
        desc += """
- Código do Conselho Tutelar: {BH}
""".format(BH=get_field(vals, 'BH'))

    if z:
        desc += """
- CNPJ: {Z}
""".format(Z=get_field(vals, 'Z'))

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
            ["AQ", "AR", "AS", "AT", "AU", "AV", "AW"]]

    now = datetime.now()

    o = Resource()
    o.name = name
    o.description = desc
    o.contact = contact
    # o.creation_date = now
    # o.creator = users[get_field(vals, 'C')]
    # o.save()
    # for t in tags:
    #     o.tags.add(t)

    print 'OK  -  ', name


def save_obj(vals):
    global count
    if get_field(vals, 'F') == 'sim':
        if get_field(vals, 'A') == 'R':
            save_resource(vals)
        elif get_field(vals, 'A') == 'O':
            # save_org(vals)
            pass
        count += 1

fname = 'importation/dados.csv'
rows = unicodecsv.reader(open(fname), encoding='utf-8')

for row in rows:
    save_obj(row)

print 'count: ', count


