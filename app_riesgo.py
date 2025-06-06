from codigo_de_ejecucion import *
import streamlit as st
from streamlit_echarts import st_echarts

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'Risk Score Analyzer',
     page_icon = 'speedometer.png',
     layout = 'wide')

#SIDEBAR
with st.sidebar:
    st.image('barralateral.webp')

    #INPUTS DE LA APLICACION
    principal = st.number_input('Loan amount', 500, 50000)
    finalidad = st.selectbox('Loan purpose', ['debt_consolidation','credit_card','home_improvement','other'])
    num_cuotas = st.radio('Installment', ['36 months','60 months'])
    ingresos = st.slider('Annual income', 20000, 300000)

    #DATOS CONOCIDOS (fijadas como datos estaticos por simplicidad)
    ingresos_verificados = 'Verified'
    antigüedad_empleo = '10+ years'
    rating = 'B'
    dti = 28
    num_lineas_credito = 3
    porc_uso_revolving = 50
    tipo_interes = 7.26
    imp_cuota = 500
    num_derogatorios = 0
    vivienda = 'MORTGAGE'

#MAIN
st.title('Risk Score Analyzer')


#CALCULAR

#Crear el registro
registro = pd.DataFrame({'ingresos_verificados':ingresos_verificados,
                         'vivienda':vivienda,
                         'finalidad':finalidad,
                         'num_cuotas':num_cuotas,
                         'antigüedad_empleo':antigüedad_empleo,
                         'rating':rating,
                         'ingresos':ingresos,
                         'dti':dti,
                         'num_lineas_credito':num_lineas_credito,
                         'porc_uso_revolving':porc_uso_revolving,
                         'principal':principal,
                         'tipo_interes':tipo_interes,
                         'imp_cuota':imp_cuota,
                         'num_derogatorios':num_derogatorios}
                        ,index=[0])



#CALCULAR RIESGO
if st.sidebar.button('calculate risks'):
    #Ejecutar el scoring
    EL = ejecutar_modelos(registro)

    #Calcular los kpis
    kpi_pd = int(EL.pd * 100)
    kpi_ead = int(EL.ead * 100)
    kpi_lgd = int(EL.lgd * 100)
    kpi_el = int(EL.principal * EL.pd * EL.ead * EL.lgd)

    #Velocimetros
    
    pd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "PD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_pd, "name": "PD"}],
                }
            ],
        }

    #Velocimetro para ead
    ead_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "EAD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_ead, "name": "EAD"}],
                }
            ],
        }

    #Velocimetro para lgd
    lgd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "LGD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10,},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_lgd, "name": "LGD"}],
                }
            ],
        }
    #Representarlos en la app
    col1,col2,col3 = st.columns(3)
    with col1:
        st_echarts(options=pd_options, width="110%", key='0')
    with col2:
        st_echarts(options=ead_options, width="110%", key='1')
    with col3:
        st_echarts(options=lgd_options, width="110%", key='2')

    #Prescripcion
    col1,col2 = st.columns(2)
    with col1:
        st.write('The expected loss is (Euros):')
        st.metric(label="Expected loss", value = kpi_el)
    with col2:
        st.write('An extra type of (Euros) is recommended:')
        st.metric(label="Commission to be Applied", value = kpi_el * 3) 

else:
    st.write('Define parameters and calculate risks')
