import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px

import os
import nltk 
from nltk.corpus import stopwords
from wordcloud import WordCloud
import re


st.title('ENTREGA FINAL')
tab1, tab2, tab3 = st.tabs(['ANALISIS DESEMPEÑO ECONOMICO', 'ANALISIS DISCURSIVO', 'ANALISIS CRITICO'])


with tab1:
    st.header('ANALISIS POR INDICADORES')

    df = pd.read_csv('Datoslimpios.csv')

    fig_Tasa_de_cambio = px.line(df, x='Fecha', y='Tasa_de_cambio', title="TRM")

    fig_PIB = px.line(df, x='Fecha',  y="PIB", title="PIB")

    fig_Inflacion = px.line(df, x='Fecha', y="Inflacion", title="INFLACION")

    fig_desempleo = px.line(df, x='Fecha', y="desempleo", title="DESEMPLEO")

    st.plotly_chart(fig_Tasa_de_cambio)
    st.write("""**(2008-2009)**
La TRM superó los 2.500 pesos por dólar, impulsada por la salida de capitales y la incertidumbre internacional.

**(2014-2015)**
La TRM subió a más de 3.000 pesos, afectada por la caída del crudo, uno de los principales productos de exportación del país.

**(2020)**
Alcanzó un récord histórico de más de 4.100 pesos por dólar, debido a la crisis global y la caída del petróleo.

**(2021)**
La incertidumbre política y fiscal mantuvo la TRM cerca de los 3.900 pesos.

**(2022-2023)**
La tasa se movió entre 3.700 y 4.000 pesos, influenciada por las reformas económicas y la cautela de los mercados.

**(2024-2025)**
Con menor inflación en EE. UU., la TRM se estabilizó entre 3.800 y 4.000 pesos, aunque sigue atenta a cambios locales.
""")
    st.plotly_chart(fig_PIB)
    st.write("""**(2008-2009)**
El crecimiento bajó de casi 6% a 1,6%, por la caída en exportaciones e inversión extranjera.

**(2015-2016)**
El fenómeno de El Niño afectó la generación de energía y la producción industrial, frenando la actividad económica.

**(2020)**
La economía se contrajo un 6,4%, con el segundo trimestre cayendo más del 15%, por el cierre de sectores productivos.

**(2023)**
El PIB apenas creció un 0,6%, afectado por inflación, altas tasas de interés y menor inversión.

**(2024-2025)**
El gasto público aumentó más rápido que los ingresos, presionando las finanzas públicas y limitando la capacidad de inversión.""")
    st.plotly_chart(fig_Inflacion)
    st.write("""**(2008-2009)**
La inflación bajó, por la menor demanda interna y la caída en los precios internacionales de alimentos y combustibles.

**(2015-2016)**
El alza del dólar y la caída del crudo dispararon los precios de productos importados y alimentos, llevando la inflación a más del 8%.

**(2020)**
La inflación se moderó al inicio por menor consumo, pero luego subió por problemas en las cadenas de suministro.

**(2022-2023)*
La inflación se disparó por la alta demanda, los costos de importación y la incertidumbre fiscal, alcanzando cifras cercanas al 13%.

**(2024-2025)**
Con las tasas de interés altas y una menor demanda, la inflación empezó a ceder, aunque se mantiene por encima de la meta del Banco de la República.""")
    st.plotly_chart(fig_desempleo)
    st.write("""**(2008-2009)**
El desempleo aumentó, superando el 12%, por la menor inversión, caída en exportaciones y recorte de empleos formales.

**(2011-2014)**
La economía creció a buen ritmo, lo que permitió bajar la tasa de desempleo a niveles cercanos al 9%.

**(2015-2016)**
Se frenó la generación de empleo, sobre todo en sectores petroleros e industriales, elevando nuevamente la tasa de desempleo.

**(2020)**
El desempleo alcanzó su nivel más alto en décadas: casi 21% en mayo de 2020, tras los cierres obligatorios y la parálisis de sectores productivos.

**(2021-2022)**
El desempleo fue cediendo gradualmente, aunque con altos niveles de informalidad, y cerró 2022 cerca del 11%.

**(2023-2024)**
La menor inversión y la incertidumbre por reformas elevaron nuevamente el desempleo, sobre todo en jóvenes y población vulnerable.""")

    dm = pd.read_csv('Datoslimpios2.csv')


    
    fig_COLCAP = px.line(dm, x='Fecha',  y="Índice COLCAP", title="COLCAP")
    st.plotly_chart(fig_COLCAP)
    st.write("""**(2008-2009)**
El índice cayó más de 30% tras la crisis internacional y la salida de capitales, marcando su primera gran caída.

**(2014-2015)**
El desplome de los precios del crudo golpeó fuerte al mercado colombiano, especialmente a Ecopetrol, y arrastró el COLCAP a la baja.

**(2020)**
En marzo de 2020, el COLCAP se desplomó a mínimos de más de una década, afectado por la crisis sanitaria y la fuerte caída del petróleo.

**(2022-2023)**
Los anuncios de cambios en política económica y energética generaron alta volatilidad, afectando particularmente acciones clave como Ecopetrol y los bancos.""")

with tab2:

    nltk.download('stopwords')

    stop_words = set(stopwords.words('spanish'))

    def procesar_texto(archivo):
        with open(archivo, "r", encoding="utf-8") as file:
            text = file.read()
        clean_text = re.sub(r'[^A-Za-záéíóúüñÁÉÍÓÚÜÑ ]', ' ', text).lower()
        words = [word for word in clean_text.split() if word not in stop_words and len(word) > 3]
        return pd.Series(words).value_counts().reset_index().rename(columns={'index': 'palabra', 0: 'frecuencia'}), ' '.join(words)

    st.title("ANALISIS DISCURSIVO")

    discursos = {
        "DISCURSO 1 AÑO PETRO.txt": "Discurso 1 Año Petro",
        "DISCURSO 2 AÑO PETRO.txt": "Discurso 2 Año Petro",
        "DISCURSO G20 PETRO.txt": "Discurso G20 Petro",
        "DISCURSO ONU PETRO.txt": "Discurso ONU Petro",
        "DISCURSO POSESION PETRO.txt": "Discurso Posesión Petro",
        "DISCURSOS COMBINADOS.txt":"Discursos combinados"
    }

    archivo = st.selectbox("Selecciona un discurso para analizar", list(discursos.keys()))
    titulo = discursos[archivo]

    df_palabras, texto_limpio = procesar_texto(archivo)
    df_top = df_palabras.head(50)

    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(texto_limpio)
    fig_wc, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Word Cloud - {titulo}", fontsize=18)

    st.pyplot(fig_wc)

with tab3:
    
    st.title('ANALISIS CRITICO')

    st.write("""1.)   Durante su gobierno Gustavo Petro ha pronunciado un gran número de discursos cuyo contenido simbólico y constantemente propositivo ha influido de sobremanera en la dinámica económica del país, que está aprendiendo a acoplarse a los anuncios espontáneos del presidente. Para facilitar el análisis nos basamos en cinco discursos clave que han caracterizado el rumbo de su gobierno, el primero de ellos es el discurso de posesión del 7 de agosto del 2022, el segundo es el discurso del primer año el 7 de agosto del 2023, el tercero es el discurso del segundo aniversario el 7 de agosto del 2024, el cuarto es el discurso ante la ONU el 24 de septiembre de 2024, y el quinto es el discurso ante la reunión del G20 el 18 de noviembre de 2024, de los cuales sustrejimos las palabras más usadas por el mandatario y los relacionamos con la dinámica económica preponderante basados en datos económicos del COLCAP, TRM, Tasa de inflación, PIB y Tasa de desempleo.  
             

**·  Discurso de posesión del 7 de agosto del 2022:**   
             
Constituyó el inicio de su gobierno, reafirmó los compromisos adquiridos en campaña y promueve espacios de concertación en pro del fortalecimiento del diálogo como forma de resolver los conflictos, dio visos de un gobierno preocupado por los pobres y excluidos de la sociedad a los que la vicepresidenta llama “los nadies”, las palabras dominantes como se muestra a continuación fueron Colombia, Paz, Vida, Pueblo, Sociedad y Economía. Sin embargo, ante un empresariado temeroso por las especulaciones de antaño de cierto sector político repercutieron negativamente en el ICOLCAP que cayó a 1228 puntos con una contracción de 3.3% mensual, en la TRM que se perfilaba al alza en $4.400, pero como un síntoma de alivio observamos que el PIB crecía al 7,3% anual, y la tasa de desempleo se ubicaba en 10,6% para agosto, una disminución del 2,3% frente al mismo mes del 2021.

**·  Discurso del primer año el 7 de agosto del 2023**
             
Ya transcurrido un año y con diversos golpes a su popularidad el presidente Petro destacó la reducción de la inflación, el aumento del salario mínimo en un 16 % y recurre mayoritariamente a palabras como Colombia, Paz, Vida, Acuerdo, Cambio, Reforma y Gobierno. Pero el panorama económico no pintaba bien, por lo menos asi lo registra el COLCAP con una reducción del 3,47% ubicandose en 1.076,12 puntos, asi como un enfriamiento en el crecimiento del PIB llegando a un precario nivel de crecimiento del 0,7% anual, por su parte la inflación bajó al 6,12% y la tasa de desempleo cayó a 9,3%.
    
**·  	Discurso del segundo aniversario el 7 de agosto del 2024**
             
Este discurso estuvo más enfocado en dar un mensaje de apoyo a las bases sociales del gobierno y en general de todo el país, ya se contaba con un panorama muy distinto de orden público, puesto que algunos grupos armados como el ELN y las disidencias de las. Las FARC de Iván Mordisco realizaban constantes ataques en contra de la población y la fuerza pública, por lo cual el presidente recurrió al uso mayoritario de las siguientes palabras Ejercito, República, Pueblo, Hoy, Libertad, Colombia. En cuanto al panorama económico el país parece que los sectores han aprendido a leer de mejor manera las volátiles propuestas del gobierno, y de alguna manera se esperaba un realce en la violencia del país, situación que por años han sufrido todos los gremios, por lo tanto en la situación del país parece impactar moderadamente el comportamiento de los mercados, el COLCAP sube 0,48% frente al mes anterior y se ubica en 1.339,79 puntos, la TRM fluctuó alrededor de $4.160, 31 COP/USD, la inflación fue el 6,12% anual, el PIB creció a un ritmo de 1,7% anual, y la tasa de desempleo registró un aumento de 0,4% frente al mismo mes del año anterior, ubicándose en 9,7%.

**·  	Discurso ante la ONU el 24 de septiembre de 2024**
             
Este discurso estuvo dirigido a promover su iniciativa de cambio de deuda por iniciativa climática, para lo que culpo a las grandes potencias del actual deterioro ambiental del mundo, no necesariamente tuvo una incidencia en el mercado colombiano, pero pudo haber dado señales negativas al sector minero y de hidrocarburos del país, las palabras más usadas por el mandatario fueron Guerra, Selva, Drogas, Planta, Poder, Acción. Siendo así el COLCAP se ubicó en 1.307 puntos con un variación mes de -2,40%, la TRM osciló entre los 4.155,31 COP/USD, la inflación se ubicó en 5,2% en 2024, lo que indica que sigue una tendencia de reducción hacia la meta de inflación, por último la tasa de desempleo fue de 9,1% en septiembre de 2024.
    
**·  	Discurso ante la reunión del G20 el 18 de noviembre de 2024**
             
Aunque también fue un mensaje guiado a la comunidad internacional, se enfocó en la temática de seguridad alimentaria resaltando a colombia como un país con potencial para ser la despensa del mundo, así como un llamado para que se materialice una reforma agraria enfocada en la producción local y sostenible, las palabras más usadas fueron Hambre, Inteligencia Artificial, Diálogo. Por su parte los indicadores económicos mostraron un panorama positivo para el país el COLCAP se ubicó en 1.392,13 puntos, la TRM se ubicó en 4.454,68 COP/USD, en el último trimestre del 2024 el PIB creció un 2.0%, y la tasa de desempleo fue del 8,2% la más baja reportada desde noviembre de 2018.


2.) Los discursos del presidente Gustavo Petro se han destacado por su alto contenido ideológico y poco técnico, lo cual genera en la mayoría de las ocasiones más incertidumbre que tranquilidad a los mercados. Si nos damos cuenta de la forma como la economía asumió el tono del mandatario, podemos establecer que, sobre todo en los discursos de sus primeros años de gobierno, solían generar menos repercusiones negativas, pero sí significativas reacciones puesto que en Colombia no se tenían antecedentes modernos de un gobierno con ideales de izquierda reformista.

Identificamos tres factores en sus discursos que nos permitieron establecer como consecuencia una tendencia volátil en los mercados a causa de sus contenidos.
              
El primero es su carácter reformista estructural, el hecho de considerar cambios a gran escala que transformen los sistemas básicos de bienestar social ya establecidos, como salud y pensiones, causan una gran incertidumbre puesto que no se contaba en ese entonces, y aún hoy en día, con una hoja de ruta clara que permitiera generar confianza en los procesos a seguir y sostenibilidad de los proyectos. Por otro lado, su enfoque económico contrario al tradicional extractivismo de recursos naturales, especialmente hidrocarburos, planteó la interrogante de ¿Cómo se reemplazarían los ingresos percibidos de la explotación?, la propuesta del presidente de fortalecer el turismo para alcanzar el mismo nivel de ingreso deja mucho que desear. 

El segundo factor, es el alto nivel de discursos “confrontativos”, el presidente ha ido fortaleciendo su discurso crítico frente al sector privado y las demás ramas del poder, especialmente la legislativa, lo que dificulta los escenarios de cooperación interinstitucional, y congestiona el ya muy polarizado escenario político.  

El tercer y último factor está relacionado con la inestabilidad institucional, evidenciado en la falta de confianza entre el ejecutivo y las cortes, así como  sus constantes roces con el Banco de la República por su política monetaria, el hecho que desde adentro del estado se haga un llamado para no acatar las decisiones propias de un equilibrio de poderes es preocupante, no solo por las consecuencias en el mercado, sino por el mensaje enviado a la sociedad como tal.

Es así como el gobierno de Gustavo Petro pasó de ser un foco de esperanza para un importante sector de la sociedad que incluía ideas de izquierda y de centro, de ser un gobierno que buscaba una unidad nacional para el avance del país, con una propuesta orientada a la consecución de la paz y la equidad, a convertirse en un grupo cerrado de funcionarios activistas sin una hoja de ruta clara, que perpetúan las prácticas clientelares y corruptas del pasado, y cuyos mensajes distribuidos en giras y particularmente en los discursos presidenciales dejan un gran interrogante sobre nuestro futuro político y sobre todo una pérdida en la confianza inversionista y promotora del crecimiento económico, que caracterizó al país.""")

