# ANTLR con Python3

## Instalación
Para la instalación de ANTLR recomiendo seguir el siguiente vídeo: [ANTLR Set up for Loading Parse Tree | Windows | English Tutorial](https://www.youtube.com/watch?v=p2gIBPz69DM)


Para Descargar la librería correspondiente en Python3
```
pip3 install antlr4-python3-runtime
```

## Comandos Útiles
Ejecución Java
```
class
antlr <nombreGramatica>.g4
javac <nombreGramatica>*.java 
grun <nombreGramatica> <reglaInicial> <programaFuente>.txt
grun <nombreGramatica> <reglaInicial> <programaFuente>.txt -gui
```

Ejecución Python3
```
class
antlr -Dlanguage=Python3 <nombreGramatica>.g4
Python3 Main.py
```
