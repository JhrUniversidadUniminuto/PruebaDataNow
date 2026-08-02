from pipeline import Pipeline

pipeline = Pipeline()

while True:

    print("\n==============================")
    print("      LOGITRACK PIPELINE")
    print("==============================")
    print("1. Generar GEO_ZONAS")
    print("2. Generar OPE_CONDUCTORES")
    print("3. Generar CLI_REMITENTES")
    print("4. Generar GPS_RUTAS")
    print("5. Generar TMS_ENVIOS")
    print("6. Generar DIR_NOVEDADES")  
    print("7. Generar CAL_DESTINATARIOS")             
    print("8. Ejecutar Todo")
    print("0. Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        pipeline.cargar_zonas()

    elif opcion == "2":
        pipeline.cargar_conductores()

    elif opcion == "3":
        pipeline.cargar_remitentes()    

    elif opcion == "4":
        pipeline.cargar_rutas()       

    elif opcion == "5":
        pipeline.cargar_envios()   

    elif opcion == "6":
        pipeline.cargar_novedades()

    elif opcion == "7":
        pipeline.cargar_calificaciones()               

    elif opcion == "8":
        pipeline.ejecutar()

    elif opcion == "0":
        print("Finalizando...")
        break

    else:
        print("Opción inválida")