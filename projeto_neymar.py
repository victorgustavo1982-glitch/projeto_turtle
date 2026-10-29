
import turtle

tela = turtle.Screen()
tela.title("Neymar Jr. - Gol!")
tela.setup(800, 600)
tela.bgcolor("black")
tela.tracer(0)

campo = turtle.Turtle()
campo.hideturtle()
campo.speed(0)
campo.color("white")
campo.pensize(3)

campo.penup()
campo.goto(-350, -220)
campo.pendown()
campo.fillcolor("green")
campo.begin_fill()

for i in range(2):
    campo.forward(700)
    campo.left(90)
    campo.forward(440)
    campo.left(90)

campo.end_fill()

campo.penup()
campo.goto(0, -220)
campo.setheading(90)
campo.pendown()
campo.forward(440)

campo.penup()
campo.goto(0, -60)
campo.setheading(0)
campo.pendown()
campo.circle(60)

campo.penup()
campo.goto(-350, -80)
campo.setheading(90)
campo.pendown()
campo.forward(160)
campo.right(90)
campo.forward(50)
campo.right(90)
campo.forward(160)

campo.penup()
campo.goto(350, -80)
campo.setheading(90)
campo.pendown()
campo.forward(160)
campo.left(90)
campo.forward(50)
campo.left(90)
campo.forward(160)

gol = turtle.Turtle()
gol.hideturtle()
gol.speed(0)
gol.color("white")
gol.pensize(5)
gol.penup()
gol.goto(250, -60)
gol.pendown()
gol.goto(250, 60)
gol.goto(320, 60)
gol.goto(320, -60)
gol.goto(250, -60)

jogador = turtle.Turtle()
jogador.hideturtle()
jogador.speed(0)
jogador.pensize(8)

jogador.penup()
jogador.goto(-220, 10)
jogador.dot(35, "#D9A066")

jogador.penup()
jogador.goto(-220, -10)
jogador.color("yellow")
jogador.pendown()
jogador.goto(-220, -55)

jogador.penup()
jogador.goto(-220, -20)
jogador.pendown()
jogador.goto(-255, 5)

jogador.penup()
jogador.goto(-220, -20)
jogador.pendown()
jogador.goto(-185, 5)

jogador.penup()
jogador.goto(-220, -55)
jogador.color("blue")
jogador.pendown()
jogador.goto(-240, -90)

jogador.penup()
jogador.goto(-220, -55)
jogador.pendown()
jogador.goto(-200, -90)

bola = turtle.Turtle()
bola.shape("circle")
bola.color("white")
bola.shapesize(1.2)
bola.penup()
bola.goto(-165, -75)
bola.speed(0)

texto = turtle.Turtle()
texto.hideturtle()
texto.penup()
texto.color("yellow")
texto.goto(0, 150)

titulo = turtle.Turtle()
titulo.hideturtle()
titulo.penup()
titulo.color("yellow")
titulo.goto(0, 245)
titulo.write("NEYMAR JR.", align="center",
             font=("Arial", 28, "bold"))

perna = turtle.Turtle()
perna.hideturtle()
perna.speed(0)
perna.color("yellow")
perna.pensize(7)

def chutar():
    perna.clear()
    perna.penup()
    perna.goto(-220, -55)
    perna.pendown()
    perna.goto(-185, -75)
    tela.update()

def mover_bola():
    bola.setx(bola.xcor() + 8)
    tela.update()

    if bola.xcor() < 270:
        tela.ontimer(mover_bola, 40)
    else:
        texto.write("GOOOOL!",
                    align="center",
                    font=("Arial", 32, "bold"))
        tela.update()

def iniciar():
    chutar()
    tela.ontimer(mover_bola, 400)

tela.update()
tela.ontimer(iniciar, 1000)

turtle.done()
