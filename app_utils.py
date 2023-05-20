import os
import os.path
from time import sleep
import pandas as pd
from datetime import datetime, time, timedelta
import sys
import shutil
from selenium import webdriver
from selenium .webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import openpyxl
import xlsxwriter
from config import userpass, mis, sro, svp, url_salvar


def ajustar_padrao_lista(valor):
    objeto = str(valor)
    objeto = str("'" + objeto + "',")
    return objeto

def ajusta_cep(valor):
    objeto = str(valor)
    objeto = objeto[0:-2]
    return objeto


def extrai_MIS(selected_date, hora_inicio, hora_fim, rampas, data, mis):

    df_postados = pd.DataFrame(columns=['Objeto', 'CEP Destino', 'Peso', 'Altura', 'Largura', 'Comprimento','Estacao'])

    navegador = webdriver.Chrome(executable_path= "./chromedriver.exe")
    sleep(1)

    navegador.get(mis)
    navegador.find_element(By.XPATH, '//*[@id="picker_1"]').clear()
    print(rf'{selected_date} {hora_inicio}')
    navegador.find_element(By.XPATH,'//*[@id="picker_1"]').send_keys(rf'{selected_date} {hora_inicio.strftime("%H:%M:%S")}')
    navegador.find_element(By.XPATH,'//*[@id="picker_2"]').clear()
    navegador.find_element(By.XPATH,'//*[@id="picker_2"]').send_keys(rf'{selected_date} {hora_fim.strftime("%H:%M:%S")}')
    print(rf'{selected_date} {hora_fim}')
    navegador.find_element(By.XPATH,'//*[@id="gosearch"]').click()

    quantidade_paginas = navegador.find_elements(By.XPATH,'//*[@id="skippage"]/option')
    quantidade_paginas = len(quantidade_paginas)


    for i in range (0,quantidade_paginas):
        select = Select(navegador.find_element(By.ID,'skippage'))
        select.select_by_index(i)
        #time.sleep(15)
        table = navegador.find_element(By.XPATH,'//*[@id="main-table"]')
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(str(table_html))
        df = df[0]
        df = df[['Object Registration number','CEP','Weight in grams','Length in millimeters', 
                 'Width in millimeters', 'Height in millimeters', 'Name of feeding station']]

        df.rename(columns=({'Object Registration number':'Objeto', 'CEP':'CEP Destino', 'Weight in grams':'Peso', 
                            'Length in millimeters':'Altura', 'Width in millimeters':'Largura', 'Height in millimeters':'Comprimento', 
                            'Name of feeding station':'Estacao'}), inplace= True)

        for rampa in rampas:
            df_rampa = df.loc[(df['Estacao']== (rf'IP{rampa.strip()}'))]
            df_postados = pd.concat([df_postados, df_rampa])


        df_postados['Objeto'] = (df_postados['Objeto'].str.rstrip())
        df_postados['Objeto'] = (df_postados['Objeto'].str.lstrip())
    navegador.quit()   



    df_postados = df_postados.drop_duplicates()
    df_postados['Motivo'] = ''
    df_postados['Observacao'] = ''
    df_postados['CEP Destino'] = df_postados['CEP Destino'].astype(str)
    df_postados['Padrão Incluir no SARA'] = [ajustar_padrao_lista(valor) for valor in df_postados['Objeto']]
    df_postados['CEP Destino'] = [ajusta_cep(valor) for valor in df_postados['CEP Destino']]

    df_postados = df_postados[['Objeto', 'Peso', 'Altura', 'Largura', 'Comprimento',
           'Estacao', 'CEP Destino','Padrão Incluir no SARA' ]]

    df_postados = df_postados.dropna()
    
    return df_postados



def pesquisa_SRO(df_postados, sro):
    
    postados = df_postados['Objeto']
    postados = postados.to_list()
    
    df_pendentes=[]
    navegador = webdriver.Chrome(executable_path= "./chromedriver.exe")

    navegador.get(sro)
    try:
        navegador.find_element(By.XPATH,'//*[@id="details-button"]').click()    
        navegador.find_element(By.XPATH,'//*[@id="proceed-link"]').click()
    except:
        pass	 

    for i in postados:
        navegador.find_element(By.XPATH,'//*[@id="objetos"]').send_keys(i)
        navegador.find_element(By.XPATH,'//*[@id="btnPesquisar"]').click()

        try:
            navegador.find_element(By.XPATH,"// td [contains (text(), 'Postado')]")
        except:
            df_pendentes.append(i)

        navegador.find_element(By.XPATH,'/html/body/form[3]/table/tbody/tr[3]/td[2]/a').click()



    df_pendentes = pd.DataFrame(zip(df_pendentes), columns=['Objeto'])

    df_pendentes = pd.merge(df_pendentes['Objeto'],df_postados[['Objeto', 'Peso', 'Altura',
                                                                'Largura', 'Comprimento','CEP Destino',
                                                                'Padrão Incluir no SARA']], on = 'Objeto', how='left' )
    
    navegador.quit()
    return df_pendentes

    
def pesquisa_SVP(df_pendentes, user, passw, svp):
   
    lista_pendentes = df_pendentes['Objeto'].to_list()
    df_pesquisa = pd.DataFrame(columns=['Objeto', 'Contrato','Cartão', 'PLP', 'Remetente'])
    navegador = webdriver.Chrome(executable_path= "./chromedriver.exe")
    navegador.get(svp[0])
    navegador.find_element(By.XPATH,'//*[@id="username"]').send_keys(user)
    navegador.find_element(By.XPATH,'//*[@id="password"]').send_keys(passw)
    navegador.find_element(By.XPATH,'//*[@id="corpo"]/div/div/div[2]/div[2]/a[1]').click()
    navegador.get(svp[1])

    for item in lista_pendentes:

        try:
            navegador.find_element(By.XPATH,'//*[@id="plp_objeto"]').send_keys(item)
            navegador.find_element(By.XPATH,'//*[@id="corpo"]/div[1]/div[2]/a').click()
            sleep(0.5)
            contrato = navegador.find_element(By.XPATH,'/html/body/section[2]/div[2]/div[3]/div[2]/div/div/div[4]/div[2]/span').text
            cartao = navegador.find_element(By.XPATH,'//*[@id="resultado"]/div/div/div[3]/div[2]/span').text
            plp = navegador.find_element(By.XPATH,'//*[@id="resultado"]/div/div/div[1]/div[2]/span').text
            remetente = navegador.find_element(By.XPATH,'//*[@id="resultado"]/div/div/div[5]/div[2]/span').text

            df_temp=pd.DataFrame({'Objeto':item, 'Contrato':contrato,'Cartão':cartao,
                                  'PLP':plp, 'Remetente':remetente}, index=[0])

        except:
            df_temp=pd.DataFrame({'Objeto':item, 'Contrato':'Objeto postal não pertence ao SIGEPWEB',
                                  'Cartão':'NA', 'PLP':'NA', 'Remetente':'NA'}, index=[0])

        navegador.find_element(By.XPATH,'//*[@id="plp_objeto"]').clear()
        sleep(0.5)
        df_pesquisa = pd.concat([df_pesquisa, df_temp])

    navegador.quit()
    
    
    df_pendentes = pd.merge( df_pendentes[['Objeto', 'Peso', 'Altura', 'Largura', 'Comprimento', 
                                           'CEP Destino','Padrão Incluir no SARA']], 
                            df_pesquisa[['Objeto', 'Contrato', 'Cartão', 'PLP',
                                         'Remetente']], on="Objeto", how='left' )
    
    df_pendentes = df_pendentes[['Objeto', 'Peso', 'Altura', 'Largura', 'Comprimento', 
                                 'CEP Destino','Contrato', 'Cartão', 'PLP', 'Remetente',
                                 'Padrão Incluir no SARA']]

    return df_pendentes
    


def cap_aut(selected_date, hora_inicio, hora_fim, rampas, data, mis, url_salvar):
    
    meses = {"January": "JANEIRO",
              "February": "FEVEREIRO",
              "March": "MARÇO",
              "April": "ABRIL",
              "May": "MAIO",
              "June": "JUNHO",
              "July": "JULHO",
              "August": "AGOSTO",
              "September": "SETEMBRO",
              "October": "OUTUBRO",
              "November": "NOVEMBRO",
              "December": "DEZEMBRO"}

    mespasta_en = data.strftime('%B')
    mespasta = meses[mespasta_en]+'_'+data.strftime('%Y')
    
    user, passw = userpass()
        
    df_postados = extrai_MIS(selected_date, hora_inicio, hora_fim, rampas, data, mis)
    
    if not df_postados.empty :    
        df_pendentes = pesquisa_SRO(df_postados, sro)
    else:
        df_pendentes = pd.DataFrame(columns=['Objeto', 'Peso', 'Altura', 'Largura', 'Comprimento', 
                                             'CEP Destino','Contrato', 'Cartão', 'PLP', 'Remetente',
                                             'Padrão Incluir no SARA'])
    
    if not df_pendentes.empty :
        df_sem_postagem = pesquisa_SVP(df_pendentes ,user, passw, svp)
    else:
        df_sem_postagem=pd.DataFrame(columns=['Objeto', 'Peso', 'Altura', 'Largura', 'Comprimento', 
                                              'CEP Destino','Contrato', 'Cartão', 'PLP', 'Remetente',
                                              'Padrão Incluir no SARA'])
    
    dia=selected_date[:2]
    mes=selected_date[3:5]
    ano=selected_date[6:]

    

    writer = pd.ExcelWriter(url_salvar(mespasta, dia, mes, ano, hora_inicio), engine='xlsxwriter')

    df_postados.to_excel(writer, sheet_name='Dados MIS', index=False) 

    df_sem_postagem.to_excel(writer, sheet_name='Pendentes de Postagem', index=False)

    writer.book.close()

    if df_sem_postagem.empty:     
        result = df_sem_postagem.empty
    else:
        result = len(df_sem_postagem)
    	
    return result