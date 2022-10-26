## TP2: Análisis de redes sociales	

grupo 18 - Arienti, Vekselman, Lakowsky, Kovo


<br>

### Estructura del repo

El repositorio cuenta con los siguientes archivos y carpetas:

- 'catedra' - Los archivos provistos por la cátedra.

- 'implementacion' - El código fuente para la solución propuesta, incluye los casos de test.

- 'experimentos' - El material correspondiente a todos los experimentos mencionados en el trabajo. Incluye scripts y archivos resultado. Se omitieron los archivos intermedios, los mismo se pueden regenerar a partir de los scripts.

- el informe.



<br>

### Nota de entorno

La compilación de los ejecutables se realizó por medio de `CMAKE` y `MAKE` en `WSL (windows)`. Recomendamos utilizar las mismas aplicaciones y trabajar en un entorno de linux. Más abajo explicamos cómo. 

Así también, los scripts se pensaron para ser ejecutados por medio de WSL. De compilar para windows ó de ejecutarse directo en linux se deberán modificar las variables globales al comienzo del archivo `./experimentos/utils/IO.py`. En el mismo se detalla cómo. 



<br>

### Cómo crear los archivos ejecutables

Para este procedimiento se asume que trabajaremos en bash. Desde la raiz del repo procederemos de la siguiente forma:

1. creamos la carpeta para los ejecutables
    > $ mkdir build
    
2. nos movemos adentro
    > $ cd build

3. creamos el cmake
    > $ cmake ../implementacion

4. creamos el ejecutable principal (el mismo se requerirá para los experimentos)
    > $ make ./tp2 

5. ejecutar

    > $ ./tp2 ../catedra/karateclub_matriz.txt 10000 1e-20

Notamos que la ejecución de los experimentos requiere que el ejecutable `./tp2` se encuentre en `./build`.


<br>

### IO ./tp2

El ejecutable del método de la potencia por deflación permite trabajar con los siguientes parámetros.


Obligatorios (deben estar en orden):

- `*` (string): fuente del archivo de entrada. El mismo puede estar formateado como una matriz o una lista de adyacencia (con ' ' como delimitador) . Si se elige este segundo formato, se deberá definir en el parametro `-f`. Ejemplo de uso: `../catedra/karateclub_matriz.txt`.

- `*` (entero): cantidad de iteraciones a realizar.

- `*` (double): tolerancia mínima aceptada.


Opcionales:

- `-f`: formato del archivo de entrada, `grafo` ó  `matriz`, por default matriz. Ejemplo de uso: `-f grafo`. 

- `-m`: representación de matriz a utilizar. `alt` ó  `base`, por default base. La representación `alt` corresponde a una matriz rala. Ejemplo de uso: `-m alt`. 

- `-o`: carpeta en la que se guardarán los archivos de salida. Por defecto, la misma donde se encuentra el ejecutable. Ejemplo de uso: `-o ../experimentos/`.

- `-as`: nombre con el que se guardarán los archivos de salida. Por defecto, este nombre será el mismo que el del archivo de entrada pero con una extensión distinta acorde al archivo a guardar. Para el archivo solución, esta extensión sera `.out`. Ejemplo de uso: `-as resultado`. 

- `-p`: la presición con la que se guardaran los resultados, en el sentido de la cantidad de digitos decimales después de la coma. Por defecto 15. Ejemplo de uso: `-p 8`.

- `-time`: Flag. Si se pasa éste parámetro, se guardará el tiempo de ejecución del algoritmo (descontando las operaciones de IO) en un archivo con la extensión `.time`.

- `-v`: Flag. Verbose. Si se pasa éste parámetro, se imprimirá en la consola información relevante durante la ejecución del programa.
