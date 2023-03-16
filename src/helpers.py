__all__ = ['barcode_to_digitable_line', 'calcular_codigo_barras']


def barcode_to_digitable_line(barcode: str):

    def modulo10(num):
        soma = 0
        peso = 2
        for c in reversed(num):
            partial = int(c) * peso
            if partial > 9:
                s = str(partial)
                partial = int(s[0]) + int(s[1])
            soma += partial
            if peso == 2:
                peso = 1
            else:
                peso = 2
        resto10 = soma % 10
        if resto10 == 0:
            md10 = 0
        else:
            md10 = 10 - resto10
        return md10

    def monta_campo(campo):
        campo_dv = "%s%s" % (campo, modulo10(campo))
        print("Valor do Campo DV, " + campo_dv )
        return "%s.%s" % (campo_dv[0:5], campo_dv[5:])

    return ' '.join([monta_campo(barcode[0:4] + barcode[19:24]),
                     monta_campo(barcode[24:34]),
                     monta_campo(barcode[34:44]),
                     barcode[4],
                     barcode[5:19]])


def calcular_codigo_barras(codigo):
    def calcular_modulo_10(codigo):
        """Calcula o dígito verificador do módulo 10 do código de barras."""
        # Separa os dígitos do código em duas partes
        primeira_parte = codigo[:-1]
        ultimo_digito = codigo[-1]

        # Calcula o dígito verificador
        soma = 0
        peso = 2
        for digito in primeira_parte[::-1]:
            soma += int(digito) * peso
            peso = 1 if peso == 2 else 2
        resto = soma % 10
        dv = 10 - resto if resto != 0 else 0

        return dv

    def calcular_modulo_11(codigo):
        """Calcula o dígito verificador do módulo 11 do código de barras."""
        # Calcula o dígito verificador
        soma = 0
        peso = 2
        for digito in codigo[::-1]:
            soma += int(digito) * peso
            if peso < 9:
                peso += 1
            else:
                peso = 2
        resto = soma % 11
        dv = 11 - resto if resto > 1 else 0

        return dv

    # Gera os campos da linha digitável
    campo_1 = f'{codigo[0:3]}.{codigo[3:4]}.{codigo[4:9]}.{codigo[9:10]}'
    campo_2 = f'{codigo[10:20]}'
    campo_3 = f'{codigo[20:24]}'
    campo_4 = f'{codigo[24:34]}'
    campo_5 = f'{codigo[34:44]}'
    dv_1 = calcular_modulo_10(campo_1)
    dv_2 = calcular_modulo_10(campo_2)
    dv_3 = calcular_modulo_10(campo_3)
    dv_4 = calcular_modulo_10(campo_4)
    dv_5 = calcular_modulo_10(campo_5)

    # Gera a linha digitável
    linha_digitavel = f'{campo_1}.{dv_1} {campo_2}.{dv_2} {campo_3}.{dv_3} {campo_4}.{dv_4} {campo_5}.{dv_5}'

    return linha_digitavel
