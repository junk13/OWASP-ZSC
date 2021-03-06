#!/usr/bin/env python
'''
OWASP ZSC | ZCR Shellcoder
https://www.owasp.org/index.php/OWASP_ZSC_Tool_Project
https://github.com/Ali-Razmjoo/OWASP-ZSC
http://api.z3r0d4y.com/
https://groups.google.com/d/forum/owasp-zsc [ owasp-zsc[at]googlegroups[dot]com ]
'''
import binascii
from core import stack
from core import color
from core.alert import info
from core.compatible import version
_version = version()
replace_values_static = {'pop %eax':'db',
		'xor %ebx,%ebx':'31 db',
		'xor %ecx,%ecx':'31 c9',
		'xor %eax,%ebx':'31 c3',
		'xor %ecx,%ebx':'31 cb',
		'xor %ebx,%eax':'31 d8',
		'xor %eax,%eax':'31 c0',
		'xor %ebx,%edx':'31 da',
		'xor %edx,%edx':'31 d2',
		'mov %esp,%ebx':'89 e3',
		'mov $0x1,%al':'b0 01',
		'mov $0x01,%al':'b0 01',
		'mov $0x1,%bl':'b3 01',
		'mov $0x01,%bl':'b3 01',
		'mov $0xb,%al':'b0 0b',
		'mov %eax,%ebx':'89 c3',
		'mov %esp,%ecx':'89 e1',
		'mov %esp,%esi':'89 e6',
		'shr $0x10,%ebx':'c1 eb 10',
		'shr $0x08,%ebx':'c1 eb 08',
		'shr $0x8,%ebx':'c1 eb 08',
		'shr $0x10,%eax':'c1 e8 10',
		'shr $0x08,%eax':'c1 e8 08',
		'shr $0x8,%eax':'c1 e8 08',
		'shr $0x10,%ecx':'c1 e9 10',
		'shr $0x8,%ecx':'c1 e9 08',
		'shr $0x08,%ecx':'c1 e9 08',
		'shr $0x10,%edx':'c1 ea 10',
		'shr $0x8,%edx':'c1 ea 08',
		'shr $0x08,%edx':'c1 ea 08',
		'inc %ecx':'41',
		'add %ecx,%ebx':'01 cb',
		'add %eax,%ebx':'01 c3',
		'add %ebx,%edx':'01 da',
		'add %ebx,%eax':'01 d8',		
		'push %eax':'50',
		'push %ebx':'53',
		'push %ecx':'51',
		'push %edx':'52',
		'push %esi':'56',
		'push %edi':'57',
		'pop %eax':'58',
		'pop %ebx':'5b',
		'pop %ecx':'59',
		'pop %edx':'5a',
		'dec %ecx':'49',
                'subl $0x61,0x3(%esp)':'83 6c 24 03 61',
                'lods %ds:(%esi),%eax':'ad',
                'add %ebx,%esi':'01 de',
                'push %esp':'54',
                'call *%edx':'ff d2',
                'call *%eax':'ff d0',
                'xchg %eax,%esi':'96',
		'mov %fs:0x30(%ecx),%eax':'64 8b 41 30',
		'mov (%esi,%ecx,2),%cx':'66 8b 0c 4e',
		'mov (%esi,%ecx,4),%edx':'8b 14 8e',
		}
def convert(shellcode):
	shellcode = shellcode.replace('\n\n','\n').replace('\n\n','\n').replace('    ',' ').replace('   ',' ')
	for data in replace_values_static:
		shellcode = shellcode.replace(data,replace_values_static[data])

	new_shellcode = shellcode.rsplit('\n')
	last = 0
	for line in new_shellcode:
		if 'push $0x' in line:
			if len(line) is 16:
				if _version is 2:
					rep = str('68') + stack.st(str(binascii.a2b_hex(str(line.rsplit('$0x')[1]))))
				if _version is 3:
					rep = str('68') + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].encode('latin-1')).decode('latin-1')))
				shellcode = shellcode.replace(line,rep)

		if 'mov $0x' in line:
			if '%ecx' in line.rsplit(',')[1]:
				if _version is 2:
					rep = str('b9') + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0])))
				if _version is 3:
					rep = str('b9') + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0].encode('latin-1')).decode('latin-1')))
				shellcode = shellcode.replace(line,rep)

		if 'mov 0x' in line:
			if '%eax' in line.rsplit(',')[0] and '%eax' in line.rsplit(',')[1]:
				rep = str('8b 40') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)
			if '%eax' in line.rsplit(',')[0] and '%esi' in line.rsplit(',')[1]:
				rep = str('8b 70') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)
			if '%eax' in line.rsplit(',')[0] and '%ebx' in line.rsplit(',')[1]:
				rep = str('8b 58') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)
			if '%ebx' in line.rsplit(',')[0] and '%edx' in line.rsplit(',')[1]:
				rep = str('8b 53') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)
			if '%edx' in line.rsplit(',')[0] and '%edx' in line.rsplit(',')[1]:
				rep = str('8b 52') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)
			if '%edx' in line.rsplit(',')[0] and '%esi' in line.rsplit(',')[1]:
				rep = str('8b 72') + stack.toHex(line.rsplit('0x')[1].rsplit('(')[0])
				shellcode = shellcode.replace(line,rep)

		if 'add' in line:
			if '$0x' in line:
				if '%esp' in line.rsplit(',')[1]:
					if _version is 2:
						rep = str('83 c4') + stack.st(str(binascii.a2b_hex(stack.toHex(line.rsplit('$0x')[1].rsplit(',')[0]))))
					if _version is 3:
						rep = str('83 c4') + stack.st(str(binascii.a2b_hex(stack.toHex(line.rsplit('$0x')[1].rsplit(',')[0]).encode('latin-1')).decode('latin-1')))
					shellcode = shellcode.replace(line,rep)

		if 'cmpl' in line:
			if '(%eax)' == line.rsplit(',')[1]:
				if _version is 2:
					rep = str('81 38') + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0])))
				if _version is 3:
					rep = str('81 38') + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0].encode('latin-1')).decode('latin-1')))
				shellcode = shellcode.replace(line,rep)
			if '0x' in line.rsplit(',')[1]:
				if '%eax' in line:
					if _version is 2:
						rep = str('81 78') + stack.st(str(binascii.a2b_hex(stack.toHex(line.rsplit(',0x')[1].rsplit('(')[0])))) + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0])))
					if _version is 3:
						rep = str('81 78') + stack.st(str(binascii.a2b_hex(stack.toHex(line.rsplit(',0x')[1].rsplit('(')[0]).encode('latin-1')).decode('latin-1'))) + stack.st(str(binascii.a2b_hex(line.rsplit('$0x')[1].rsplit(',')[0].encode('latin-1')).decode('latin-1')))
					shellcode = shellcode.replace(line,rep)

		if 'jne' in line:
			rep = str('75') + hex(int('f4', 16) - last*9)[2:]
			shellcode = shellcode.replace(line,rep,1)
			last += 1
	shellcode = stack.shellcoder(shellcode.replace('\n','').replace(' ',''))
	return shellcode
