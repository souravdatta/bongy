'''
Under MIT License. Please see accompanying LICENSE document.
'''
import re

class HTMLGen:
    html_template = '''
        <!doctype html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style>
                td {{
                    position: relative;
                    display: block;
                    width: 60px;
                    height: 20px;
                    margin: 4px;
                    padding: 4px;
                    float: left;
                    text-align: center;
                }}

                .border {{
                    border: 1px solid black;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <center>
            <table>
                <tr>
                    <td class="border">{{}}</td>
                    <td>Group letters
                </tr>
                {0}
            </table>
            </center>
        </body>
        </html>
    '''

    def gen_mapping_html(self, maps):
        content = ''
        for l, m in sorted(maps.items()):
            content += '''
                <tr>
                    <td class="border">{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                </tr>'''.format(l, m['r'] if 'r' in m else '', m['m'] if 'm' in m else '')
        return self.html_template.format(content)

class Converter:
    ignore_list = [r' ,.;?\'\"[]{}()']

    char_maps = {
        'a1': {'m': '\u0981'},
        'a2': {'m': '\u0982'},
        'a3': {'m': '\u0983'},
        'a4': {'m': '\u09C3'},
        'a5': {'m': '\u09F4'},
        'a6': {'m': '\u09CD\u09AF'},
        'a': {'r': '\u0985', 'm': '\u0985'},
        'A': {'r': '\u0986', 'm': '\u09BE'},
        'i': {'r': '\u0987', 'm': '\u09BF'},
        'I': {'r': '\u0988', 'm': '\u09C0'},
        'u': {'r': '\u0989', 'm': '\u09C1'},
        'U': {'r': '\u098A', 'm': '\u09C2'},
        'e': {'r': '\u098F', 'm': '\u09C7'},
        'E': {'r': '\u0990', 'm': '\u09C8'},
        'o': {'r': '\u0993', 'm': '\u09CB'},
        'O': {'r': '\u0994', 'm': '\u09CC'},
        'k': {'r': '\u0995'},
        'K': {'r': '\u0996'},
        'g': {'r': '\u0997'},
        'G': {'r': '\u0998'},
        'n1': {'r': '\u0999'},
        'c': {'r': '\u099A'},
        'C': {'r': '\u099B'},
        'j': {'r': '\u099C'},
        'J': {'r': '\u099D'},
        'n2': {'r': '\u099E'},
        't': {'r': '\u099F'},
        'T': {'r': '\u09A0'},
        'd': {'r': '\u09A1'},
        'D': {'r': '\u09A2'},
        'N': {'r': '\u09A3'},
        't1': {'r': '\u09A4'},
        'T1': {'r': '\u09A5'},
        'd1': {'r': '\u09A6'},
        'D1': {'r': '\u09A7'},
        'n': {'r': '\u09A8'},
        'p': {'r': '\u09AA'},
        'P': {'r': '\u09AB'},
        'b': {'r': '\u09AC'},
        'B': {'r': '\u09AD'},
        'm': {'r': '\u09AE'},
        'z': {'r': '\u09AF'},
        'r': {'r': '\u09B0'},
        'R1': {'r': '\u09E0'},
        'l': {'r': '\u09B2'},
        'S': {'r': '\u09B6'},
        's1': {'r': '\u09B7'},
        's': {'r': '\u09B8'},
        'h': {'r': '\u09B9'},
        'R': {'r': '\u09DC'},
        'r1': {'r': '\u09DD'},
        'y': {'r': '\u09DF'},
        'n3': {'r': '\u09FA'},
        't2': {'r': '\u09CE'}
    }

    def convert(self, frms):
        parts = re.findall(r'(\{.+?\})|(\w\d)|(.)', frms)
        rparts = []
        for p in parts:
            if p[0] != '':
                rparts.append(p[0])
            elif p[1] != '':
                rparts.append(p[1])
            elif p[2] != '':
                rparts.append(p[2])
            else:
                rparts.append(p[0]+ p[1] + p[2])
        convs = ''
        for i in rparts:
            gs = re.search(r'^\{(.*?)\}$', i)
            if gs is not None:
                convs += self.convert_compound(gs.group(1))
            else:
                if i in self.char_maps:
                    convs += self.char_maps[i]['r']
                else:
                    convs += i
        return convs

    def isword(self, c):
        return re.match(r'[a-zA-Z]', c)

    def isconsonant(self, c):
        return self.isword(c) and re.match(r'[^aeiou]', c, re.I) is not None

    def iscomposer(self, c):
        return (c in self.char_maps) and (re.match(r'[aeiou][0-9]?', c, re.I))

    def lookup(self, c, m=False):
        if c in self.char_maps:
            return self.char_maps[c]['r' if not m else 'm']
        return c

    def convert_compound(self, frms):
        stk = []
        skipped = False
        for i in range(0, len(frms)):
            if skipped:
                skipped = False
                continue
            c = frms[i]
            if i < (len(frms) - 1) and (frms[i+1] in '1234567890'):
                c += frms[i+1]
                skipped = True
            if self.isconsonant(c):
                if i > 0:
                    stk.append('\u09CD')
                stk.append(self.lookup(c))
            elif self.iscomposer(c) and (i > 0):
                stk.append(self.lookup(c, m=True))
            elif self.iscomposer(c) and (i == 0):
                stk.append(self.lookup(c))
            else:
                stk.append(c)
        return ''.join(stk)

    def gen_mapping(self):
        ghtml = HTMLGen()
        return ghtml.gen_mapping_html(self.char_maps)
