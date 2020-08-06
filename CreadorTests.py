import os

os.chdir(r"I:\Descargas 2.0\tests")
for file in os.listdir(os.getcwd()):
    num,ext=file.split(".")
    if ext=="in":
        entrada=open(file,"r")
        salida=open(num+".out")
        p1="self.assertEqual(Iniciar("
        p2=""
        for i in entrada.readlines():
            p2=p2+"\""+ "".join(i).rstrip("\n") +"\","
        p1=p1+p2
        p1=list(p1)
        p1[-1]="),["
        p1="".join(p1)
        #Ahora va la matriz
        necesario=True
        for i in salida.readlines():
            if i=="IMPOSIBLE":
                p1 = list(p1)
                p1[-1] = ""
                p1 = "".join(p1)
                p1=p1+'"IMPOSIBLE"'
                necesario=False
            else:
                nums=i.rstrip("\n").split()
                for j in range(0,len(nums)):
                    nums[j]="'"+str(nums[j])+"'"
                p1=p1+"["+",".join(nums)+"]"+","
        if necesario:
            p1 = list(p1)
            p1[-1] = ""
            p1 = "".join(p1)
            p1=p1+"])"
        else:
            p1=p1+")"
        entrada.close()
        salida.close()
        print(p1)
    else:
        pass


