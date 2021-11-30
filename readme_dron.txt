                       **********
                       ** DRON **
                       **********
         El programilla para matar el rato by JC


1.- Requerimientos

Aparte de Python3 (puedes bajarlo de www.python.org), el 
programa usa las librerías NumPy & PyGame. Si no las tienes
instálalas (pip3 install pygame ó lo que sea). Para lanzar 
el juego usa el comando "python3 dron.py" o bien
"python dron.py" dependiendo de tu instalación. Si no estás 
en el directorio del juego ("dron_distrib" salvo que lo hayas
cambiado, tendrás que poner el path completo al archivo dron.py

El juego intentará crear una ventana de 1200x900 pixeles, que
es su resolución nativa. Si tu monitor no tiene suficiente 
capacidad se creará la ventana que sea posible y el juego se 
adaptará a ella. Cabe esperar algún inconveniente menor en 
ese caso (figuras menos nítidas y distinto tacto de control). 


2.- Objeto del juego

Tu dron está en campo enemigo con la misión de fotografíar 
sus bases y eventualmente su armamento móvil (panzers). Para 
sacar una foto el dron debe estar completamente encima de la 
base y con poca velocidad. Basta con que esas condiciones 
ocurran un instante para que la foto se tome automáticamente. 
Se oye un click y la base se oscurece. La foto a un panzer 
transcurre similarmente salvo que el dron puede tener 
cualquier velocidad.

Una vez fotografíadas todas las bases y panzers, aparece la 
plataforma de rescate. El dron debe aterrizar en ella con una 
velocidad pequeña que debe ser puramente horizontal.

El dron tiene una cierta autonomía (creciente con el nivel),
y la misión debe completarse sin sobrepasarla. Como aviso, 
cuando se llega a la mitad de la autonomía el dron cambia a 
color amarillo, y cuando se llega a sus tres cuartas partes 
se vuelve marrón.

Por supuesto las bases dispararán misiles de cabeza buscadora 
y los panzers dispararán balas al dron. Momentos antes de 
producirse un disparo el elemento correspondiente se vuelve 
rojo. El nivel de kung-fu que te pregunta al principio afecta
ligeramente a la frecuencia de disparos y a otros parámetros.

Si necesitas pausar el juego pulsa la barra espaciadora. La
ventana se minimiza (por si viene tu jefe) y los sonidos
se detienen. Para terminar el juego simplemente cierra la 
ventana.


3.- Control del dron

El dron se controla con las cuatro flechas del teclado. Su 
velocidad aumenta (hasta un límite) en cada dirección y 
sentido coincidiendo con los de las flechas. Para un control 
más fino de la velocidad es aconsejable dar toques de tecla 
individuales en lugar de mantener pulsada la tecla. 


4.- Consejos para el juego

El dron es muy maniobrable, lo cual es conveniente pero 
conlleva cierta dificultad en el manejo. Es buena idea 
dedicar los primeros momentos con el juego a intentar parar 
el dron, a hacer que vaya despacio (internamente hay cinco 
velocidades en cada dirección), a intentar que solo tenga 
velocidad horizontal o vertical, etc

El dron puede detenerse en poco espacio desde su velocidad 
máxima. Ello permite acercarse rápidamente a una base y 
frenar muy cerca de ella (o prácticamente sobre ella) antes 
de sacar la foto. Seguramente encuentres este procedimiento 
más ventajoso que sobrevolar lento y pulsar nerviosamente 
las flechas sin conseguir la poca velocidad requerida.


5.- Licencia

El autor ofrece el juego Dron como software libre bajo 
licencia GPL v3. Básicamente puedes usar el programa, hacer 
copias, distribuírlas libremente, estudiar el código y hacer
modificaciones o mejoras al mismo. En este último caso, si se
hace público el programa modificado, debe hacerse bajo la 
misma licencia GPL, y mencionar al autor original como tal. 
Consulte la cabecera del programa para más detalles.

Espero que Dron sea de su agrado. El Autor:
                       Juan Carlos del Caño 
____________________________________________



