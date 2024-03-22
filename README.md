# Pychon

Pequeña aplicación de chat para enviar marcos (frames) a nivel de enlace (nivel 2).

Los mensajes se envían (difunden) por broadcast (`FF:FF:FF:FF:FF:FF`) codificados en UTF-8 y con EtherType `0x1234`.

## Uso

Para iniciar la recepción de mensajes:

```bash
python chat.py --receive [interfaz]
```

> Siendo `interfaz` la interfaz de red por la que se van recibir los mensajes.

Para enviar mensajes:

```bash
python chat.py --send
```

La opción `--send` inicia la aplicación en modo interactivo, de modo que se pueden enviar tantos mensajes como se desee a través de la red.

## Dependencias

Crear un entorno virtual:

```bash
python -m venv venv
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Para generar el fichero de dependencias (en caso de que sea necesario):

```bash
pip freeze > requirements.txt
```


