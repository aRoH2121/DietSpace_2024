from models import peso

def init_db():
    pesi={
        "Peso" : [81.4, 77.3, 83.5],
        "DataInserimentoPeso" : ['12/04/2024', '14/05/2024', '14/06/2024'],
        "emailPaziente_id" : ['franci@gmail.com', 'ciao', 'franci@gmail.com'],
    }
    for i in range(3):
        p = peso()
        for j in pesi:
            if j == 'Peso':
                p.Peso = pesi[j][i]
            if j == 'DataInserimentoPeso':
                p.DataInserimentoPeso = pesi[j][i]
            if j == 'emailPaziente_id':
                p.emailPaziente = pesi[j][i]
        p.save()

print("DUMP DB")
print(peso.objects.all())


    # alim = {
    #     "nome" : ["pasta","riso","pane","pollo","tonno","merluzzo","peperoni","zucchine","porcodio"],
    #     "proteine" : [14.0,12.2,6.1,22.1,18.9,16.0,0.8,1.1,2.2],
    #     "grassi" : [4.0,2.4,2.1,0.1,0.7,3.1,0.1,0.2,3.4],
    #     "carboidrati" : [45.2,48.0,35.6,4.3,3.1,2.1,5.1,0.2,5.3],
    #     "calorie" : [354.0,320.0,350.0,110.0,100.0,120.0,60.2,40.0,3232.3],
    # }

    # for i in range(9):
    #     a = alimento()
    #     for j in alim:
    #         if j == "nome":
    #             a.nome = alim[j][i]
    #         if j == "proteine":
    #             a.proteine = alim[j][i]
    #         if j == "grassi":
    #             a.grassi = alim[j][i]
    #         if j == "carboidrati":
    #             a.carboidrati = alim[j][i]
    #         if j == "calorie":
    #             a.calorie = alim[j][i]
    #     a.save()

    # print("DUMP DB")
    # print(alimento.objects.all())
    