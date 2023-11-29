# Cluster
# Diseño del Sistema
# Servidor Principal:

# Espera y acepta conexiones de clientes.
# Recibe un video del cliente.
# Divide el video en clips.
# Envía cada clip a un servidor esclavo diferente.
# Recibe los clips procesados de los servidores esclavos.
# Combina los clips procesados.
# Envía el video final procesado de vuelta al cliente.
# Servidor Esclavo (para procesamiento de clips):

# Recibe clips de video del servidor principal.
# Procesa el clip (este paso depende de lo que necesites hacer con el video).
# Envía el clip procesado de vuelta al servidor principal.