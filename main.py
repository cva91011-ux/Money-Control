from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from database import obtener_fondo, guardar_fondo
from kivy.uix.filechooser import FileChooserListView
from database import guardar_fondo
from kivy.uix.floatlayout import FloatLayout
from database import obtener_fondo
import csv
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
import os
import shutil

from database import (
    obtener_saldo,
    cambiar_saldo,
    guardar_movimiento,
    obtener_historial,
    obtener_patron,
    cambiar_patron,
    obtener_gastos_categoria
)

class PantallaBase(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.capa = FloatLayout()


        self.fondo = Image(
            source=obtener_fondo(),
            allow_stretch=True,
            keep_ratio=False
        )


        self.capa.add_widget(self.fondo)


        self.contenido = BoxLayout(
            orientation="vertical"
        )


        self.capa.add_widget(self.contenido)


        self.add_widget(self.capa)

class Bloqueo(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        caja = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=40
        )


        titulo = Label(
            text="🔐 MONEY MANAGER\n\nIngrese patrón",
            font_size=30
        )

        caja.add_widget(titulo)


        self.entrada = TextInput(
            hint_text="Patrón",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=60
        )

        caja.add_widget(self.entrada)


        boton = Button(
            text="Entrar",
            size_hint_y=None,
            height=60
        )


        boton.bind(
            on_press=self.verificar
        )


        caja.add_widget(boton)


        self.mensaje = Label()

        caja.add_widget(self.mensaje)


        self.add_widget(caja)



    def verificar(self, boton):

        if self.entrada.text == obtener_patron():

            self.manager.current="inicio"

            self.entrada.text=""
            self.mensaje.text=""

        else:

            self.mensaje.text="❌ Patrón incorrecto"

            self.entrada.text=""
class Inicio(PantallaBase):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        caja = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=30
        )


        titulo = Label(
            text="Bienvenido a\nMONEY MANAGER",
            font_size=30
        )

        caja.add_widget(titulo)



        botones = [
            ("💰 Ingreso","ingreso"),
            ("💸 Retiro","retiro"),
            ("📜 Historial","historial"),
            ("📊 Gráfica","grafica"),
            ("⚙ Opciones","opciones")
        ]



        for texto, pantalla in botones:

            boton = Button(
                text=texto,
                size_hint_y=None,
                height=60
            )


            boton.bind(
                on_press=lambda x,p=pantalla:
                setattr(self.manager,"current",p)
            )


            caja.add_widget(boton)



        # AQUÍ TERMINA EL FOR


        self.tarjetas = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            height=200
        )


        self.saldo_fisico = Label(
            text="💵 Dinero físico\nC$ 0",
            font_size=22
        )


        self.saldo_digital = Label(
            text="💳 Dinero digital\n$ 0",
            font_size=22
        )


        self.tarjetas.add_widget(
            self.saldo_fisico
        )


        self.tarjetas.add_widget(
            self.saldo_digital
        )


        caja.add_widget(
            self.tarjetas
        )



        self.contenido.add_widget(caja)



    def on_pre_enter(self):

        fisico, digital = obtener_saldo()


        self.saldo_fisico.text = f"""
💵 DINERO FÍSICO

C$ {fisico:.2f}
"""


        self.saldo_digital.text = f"""
💳 DINERO DIGITAL

$ {digital:.2f}
"""
class Ingreso(PantallaBase):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        caja = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20
        )


        caja.add_widget(
            Label(
                text="INGRESO",
                font_size=30
            )
        )


        self.monto = TextInput(
            hint_text="Cantidad",
            multiline=False
        )

        caja.add_widget(self.monto)



        btn1 = Button(
            text="Ingreso Digital USD"
        )

        btn1.bind(
            on_press=lambda x:self.guardar("USD")
        )

        caja.add_widget(btn1)



        btn2 = Button(
            text="Ingreso Físico NIO"
        )

        btn2.bind(
            on_press=lambda x:self.guardar("NIO")
        )

        caja.add_widget(btn2)



        volver = Button(
            text="Volver"
        )

        volver.bind(
            on_press=lambda x:
            setattr(self.manager,"current","inicio")
        )

        caja.add_widget(volver)


        self.contenido.add_widget(caja)



    def guardar(self, moneda):

        cantidad = float(self.monto.text)


        fisico,digital = obtener_saldo()


        if moneda=="NIO":

            fisico += cantidad

        else:

            digital += cantidad



        cambiar_saldo(
            fisico,
            digital
        )


        guardar_movimiento(
            "Ingreso",
            "Ingreso",
            cantidad,
            moneda,
            "Ingreso"
        )


        self.monto.text=""

class Retiro(PantallaBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        caja = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20
        )

        caja.add_widget(
            Label(
                text="RETIRO",
                font_size=30
            )
        )

        self.monto = TextInput(
            hint_text="Cantidad",
            multiline=False
        )
        caja.add_widget(self.monto)

        self.motivo = TextInput(
            hint_text="Motivo del gasto",
            multiline=False
        )
        caja.add_widget(self.motivo)

        self.categoria = Spinner(
            text="Elegir categoría",
            values=(
                "Comida",
                "Transporte",
                "Compras",
                "Servicios",
                "Otros"
            ),
            size_hint_y=None,
            height=60
        )
        caja.add_widget(self.categoria)

        btn1 = Button(
            text="Retiro Digital USD"
        )
        btn1.bind(
            on_press=lambda x: self.retirar("USD")
        )
        caja.add_widget(btn1)

        btn2 = Button(
            text="Retiro Físico NIO"
        )
        btn2.bind(
            on_press=lambda x: self.retirar("NIO")
        )
        caja.add_widget(btn2)

        volver = Button(
            text="Volver"
        )
        volver.bind(
            on_press=lambda x: setattr(self.manager, "current", "inicio")
        )
        caja.add_widget(volver)

        self.contenido.add_widget(caja)

    def retirar(self, moneda):

        try:
            cantidad = float(self.monto.text)
        except ValueError:
            return

        motivo = self.motivo.text.strip()
        categoria = self.categoria.text

        fisico, digital = obtener_saldo()

        if moneda == "NIO":
            fisico -= cantidad
        else:
            digital -= cantidad

        cambiar_saldo(fisico, digital)

        guardar_movimiento(
            motivo,
            categoria,
            cantidad,
            moneda,
            "Retiro"
        )

        self.monto.text = ""
        self.motivo.text = ""
        self.categoria.text = "Elegir categoría"


class Historial(PantallaBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lista = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10,
            size_hint_y=None
        )

        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        self.contenido.add_widget(scroll)

    def on_pre_enter(self):

        self.lista.clear_widgets()

        datos = obtener_historial()

        for x in datos:

            tarjeta = Label(
                text=f"""📅 {x[1]}
⏰ {x[2]}

📝 Motivo:
{x[3]}

📂 Categoría:
{x[4]}

💰 Monto:
{x[5]} {x[6]}

📌 Tipo:
{x[7]}
""",
                font_size=16,
                size_hint_y=None,
                height=220
            )

            self.lista.add_widget(tarjeta)
class Pagina(Screen):

    def __init__(self,texto,**kwargs):

        super().__init__(**kwargs)

        self.add_widget(
            Label(
                text=texto,
                font_size=25
            )
        )


class Grafica(PantallaBase):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.caja = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20
        )


        self.info = Label(
            font_size=18
        )

        self.caja.add_widget(self.info)


        self.imagen = Image()

        self.caja.add_widget(self.imagen)



        boton = Button(
            text="💰 Ver distribución dinero",
            size_hint_y=None,
            height=60
        )

        boton.bind(
            on_press=lambda x: self.crear_grafica()
        )

        self.caja.add_widget(boton)



        boton2 = Button(
            text="📊 Ver gastos por categoría",
            size_hint_y=None,
            height=60
        )


        boton2.bind(
            on_press=lambda x: self.crear_grafica_gastos()
        )


        self.caja.add_widget(boton2)



        volver = Button(
            text="Volver",
            size_hint_y=None,
            height=60
        )


        volver.bind(
            on_press=lambda x:
            setattr(self.manager,"current","inicio")
        )


        self.caja.add_widget(volver)



        self.contenido.add_widget(self.caja)



    def crear_grafica(self):

        fisico, digital = obtener_saldo()


        cambio = 36.50


        digital_nio = digital * cambio


        total = fisico + digital_nio



        if total == 0:

            porcentaje_fisico = 0
            porcentaje_digital = 0

        else:

            porcentaje_fisico = (fisico / total) * 100

            porcentaje_digital = (digital_nio / total) * 100



        plt.figure(figsize=(5,5))


        plt.pie(
            [
                fisico,
                digital_nio
            ],

            labels=[
                f"Físico NIO {porcentaje_fisico:.1f}%",
                f"Digital USD {porcentaje_digital:.1f}%"
            ],

            autopct="%1.1f%%"
        )


        plt.title(
            "Distribución del dinero"
        )


        plt.savefig(
            "grafica.png"
        )


        plt.close()


        self.imagen.source = "grafica.png"


        self.info.text = f"""
SALDO ACTUAL

💰 Físico:
C$ {fisico:.2f}


💳 Digital:
$ {digital:.2f}


Total equivalente:

C$ {total:.2f}
"""



    def crear_grafica_gastos(self):


        datos = obtener_gastos_categoria()


        if len(datos) == 0:

            self.info.text = "No hay gastos registrados"

            return



        categorias = []

        montos = []



        for dato in datos:

            categorias.append(
                dato[0]
            )

            montos.append(
                dato[1]
            )



        plt.figure(figsize=(5,5))


        plt.pie(
            montos,
            labels=categorias,
            autopct="%1.1f%%"
        )


        plt.title(
            "Gastos por categoría"
        )


        plt.savefig(
            "gastos.png"
        )


        plt.close()



        self.imagen.source = "gastos.png"


        self.info.text = "Distribución de gastos"

class Opciones(PantallaBase):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        caja = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=30
        )


        caja.add_widget(
            Label(
                text="OPCIONES",
                font_size=30
            )
        )


        boton_fondo = Button(
            text="🖼 Cambiar fondo",
            size_hint_y=None,
            height=60
        )

        boton_fondo.bind(
            on_press=self.mostrar_selector
        )

        caja.add_widget(boton_fondo)



        claro = Button(
            text="☀ Tema claro",
            size_hint_y=None,
            height=60
        )

        claro.bind(
            on_press=lambda x:self.tema_claro()
        )

        caja.add_widget(claro)



        oscuro = Button(
            text="🌙 Tema oscuro",
            size_hint_y=None,
            height=60
        )

        oscuro.bind(
            on_press=lambda x:self.tema_oscuro()
        )

        caja.add_widget(oscuro)



        titulo_patron = Label(
            text="🔐 Cambiar patrón",
            font_size=20
        )

        caja.add_widget(titulo_patron)



        self.nuevo_patron = TextInput(
            hint_text="Nuevo patrón",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=60
        )

        caja.add_widget(self.nuevo_patron)



        guardar = Button(
            text="Guardar patrón",
            size_hint_y=None,
            height=60
        )

        guardar.bind(
            on_press=self.guardar_patron
        )

        caja.add_widget(guardar)



        respaldo = Button(
            text="💾 Crear copia de seguridad",
            size_hint_y=None,
            height=60
        )

        respaldo.bind(
            on_press=self.crear_respaldo
        )

        caja.add_widget(respaldo)



        exportar = Button(
            text="📄 Exportar historial CSV",
            size_hint_y=None,
            height=60
        )

        exportar.bind(
            on_press=self.exportar_csv
        )

        caja.add_widget(exportar)



        volver = Button(
            text="Volver",
            size_hint_y=None,
            height=60
        )

        volver.bind(
            on_press=lambda x:
            setattr(self.manager,"current","inicio")
        )

        caja.add_widget(volver)



        self.contenido.add_widget(caja)



    def guardar_patron(self, boton):

        nuevo = self.nuevo_patron.text


        if nuevo:

            cambiar_patron(nuevo)

            self.nuevo_patron.text=""



    def mostrar_selector(self, boton):

        selector = FileChooserListView()


        seleccionar = Button(
            text="Usar imagen",
            size_hint_y=None,
            height=60
        )


        ventana = BoxLayout(
            orientation="vertical"
        )


        ventana.add_widget(selector)

        ventana.add_widget(seleccionar)


        popup = Popup(
            title="Seleccionar fondo",
            content=ventana,
            size_hint=(0.9,0.9)
        )


        seleccionar.bind(
            on_press=lambda x:
            self.guardar_imagen(
                selector.selection,
                popup
            )
        )


        popup.open()



    def guardar_imagen(self, seleccion, popup):

        if seleccion:

            guardar_fondo(
                seleccion[0]
            )

            popup.dismiss()



    def crear_respaldo(self, boton):

        origen = "money.db"

        destino = "backup_money.db"


        if os.path.exists(origen):

            shutil.copy(
                origen,
                destino
            )



    def exportar_csv(self, boton):

        datos = obtener_historial()


        with open(
            "historial_money.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:


            escritor = csv.writer(archivo)


            escritor.writerow(
                [
                    "Fecha",
                    "Hora",
                    "Motivo",
                    "Categoria",
                    "Monto",
                    "Moneda",
                    "Tipo"
                ]
            )


            for fila in datos:

                escritor.writerow(
                    [
                        fila[1],
                        fila[2],
                        fila[3],
                        fila[4],
                        fila[5],
                        fila[6],
                        fila[7]
                    ]
                )



    def tema_oscuro(self):

        Window.clearcolor=(
            0.05,
            0.05,
            0.05,
            1
        )



    def tema_claro(self):

        Window.clearcolor=(
            1,
            1,
            1,
            1
        )




class MoneyManager(App):

    def build(self):

        sm = ScreenManager()


        sm.add_widget(
            Bloqueo(name="bloqueo")
        )


        sm.add_widget(
            Inicio(name="inicio")
        )


        sm.add_widget(
            Ingreso(name="ingreso")
        )


        sm.add_widget(
            Retiro(name="retiro")
        )


        sm.add_widget(
            Historial(name="historial")
        )


        sm.add_widget(
            Grafica(name="grafica")
        )


        sm.add_widget(
            Opciones(name="opciones")
        )


        sm.current = "bloqueo"


        return sm



    def on_pause(self):

        self.root.current = "bloqueo"

        return True



    def on_resume(self):

        self.root.current = "bloqueo"