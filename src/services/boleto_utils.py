"""
Boleto de Arrecadação Bancária / Banco
https://portal.febraban.org.br/pagina/3166/33/pt-br/layour-arrecadacao
https://www.bb.com.br/docs/pub/emp/mpe/dwn/PadraoCodigoBarras.pdf
https://www.ttrix.com/apple/iphone/boletoscan/boletoanatomia.html

Codigos
https://github.com/mrmgomes/boleto-utils/blob/master/src/boleto-utils.js
https://github.com/rruy/validacao-linha-digitavel-boletos-ruby/blob/master/concessionaire_boleto_validator.rb
https://github.com/jardelgoncalves/broleto/blob/master/src/Boleto/index.ts
"""

class BoletoUtils:

    def _modulo10(self, num: str):
        if not isinstance(num, str):
            raise TypeError
        soma = 0
        peso = 2
        for c in reversed(num):
            parcial = int(c) * peso
            if parcial > 9:
                s = str(parcial)
                parcial = int(s[0]) + int(s[1])
            soma += parcial
            if peso == 2:
                peso = 1
            else:
                peso = 2

        resto10 = soma % 10
        if resto10 == 0:
            modulo10 = 0
        else:
            modulo10 = 10 - resto10

        return modulo10
    
    def _modulo11(self, num: str, base=9, r=0):
        if not isinstance(num, str):
            raise TypeError
        soma = 0
        fator = 2
        for c in reversed(num):
            soma += int(c) * fator
            if fator == base:
                fator = 1
            fator += 1
        if r == 0:
            soma = soma * 10
            digito = soma % 11
            if digito == 10:
                digito = 0
            return digito
        if r == 1:
            resto = soma % 11
            return resto

    def _verifica_modulo_calculo_arrecadacao(self, codigo_de_barra: str):
        return self._modulo10 if codigo_de_barra[2] == '6' or codigo_de_barra[2] == '7' else self._modulo11

    def _monta_bloco_bancario(self, bloco: str):
        campo_dv = bloco + str(self.modulo10(bloco))
        return f"{campo_dv[0:5]}.{campo_dv[5:]}"

    def _verifica_tipo_boleto(self, codigo_de_barra):
        if len(codigo_de_barra) != 44:
            raise Exception('Código de barras inválido')
        return 'ARRECADACAO' if codigo_de_barra[0] == '8' else 'BANCO'

    def calcula_ld_arrecadacao(self, codigo_de_barra: str):
        modulo_calcular = self._verifica_modulo_calculo_arrecadacao(codigo_de_barra)
        bloco1 = codigo_de_barra[0:11]
        bloco1 = bloco1 + str(modulo_calcular(bloco1))
        bloco2 = codigo_de_barra[11:22]
        bloco2 = bloco2 + str(modulo_calcular(bloco2))
        bloco3 = codigo_de_barra[22:33]
        bloco3 = bloco3 + str(modulo_calcular(bloco3))
        bloco4 = codigo_de_barra[33:44]
        bloco4 = bloco4 + str(modulo_calcular(bloco4))
        return " ".join([bloco1, bloco2, bloco3, bloco4])

    def calcula_ld_banco(self, codigo_de_barra: str):
        bloco1 = codigo_de_barra[0:4] + codigo_de_barra[19:24]
        bloco2 = codigo_de_barra[24:34]
        bloco3 = codigo_de_barra[34:44]
        bloco4 = codigo_de_barra[4]
        bloco5 = codigo_de_barra[5:19]
        return " ".join([self._monta_bloco_bancario(bloco1), self._monta_bloco_bancario(bloco2), self._monta_bloco_bancario(bloco3), bloco4, bloco5])

    def calcula_linha_digitavel(self, codigo_de_barra):
        tipo_boleto = self._verifica_tipo_boleto(codigo_de_barra)
        if tipo_boleto == 'ARRECADACAO':
            return self.calcula_ld_arrecadacao(codigo_de_barra)
        if tipo_boleto == 'BANCO':
            return self.calcula_ld_banco(codigo_de_barra)
        raise Exception('Não existe linha digitavel implementada para esse codigo de barras')


def main():
    codigo_de_barra = "84660000000578800601000132079294392212983786"
    boletoutils = BoletoUtils()
    print(boletoutils.calcula_linha_digitavel(codigo_de_barra=codigo_de_barra))


    

if __name__ == '__main__':
    main()