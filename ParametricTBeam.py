# Save by TommyHielscher on 2022_04_12-13.19.16; build 2021 2020_03_07-01.50.37 167380
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import time

# ====================== Working Look ========================

t_file = open('C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/number_of_sols.txt','r')
num_it  = t_file.read()
num_it = num_it.split(' ')
iterations = int(num_it[0])
print("Number of simulations required: " + str(iterations))

sol = 1
while True:

    # ====================== Set Directory ======================

    os.chdir(
        r"C:\Users\TommyHielscher\Desktop\Abaqus_scripting\ReinforcedTBeam\Parametric")

    session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

    # ====================== Locked parameters ======================


    # ====================== Define parameters ====================== 
    param_file = 'C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/parameters.txt'
    
    while True:
        time.sleep(0.5)
        
        file_p = open(param_file,'r')
        data = file_p.read()
        data = data.split(',')
          
        Depth_Mid = float(data[0])
        Width_Mid = float(data[1])
        Overhang_Width = float(data[2])
        Top_Thickness = float(data[3])
        Dist_Top_Long = float(data[4])
        Transverse_Length = Overhang_Width*2 + Width_Mid
        
        phase = data[-1]
        
        if phase == "newdata":
            print("New data found!")
            break
        else:
            print("Waiting for new data")

    
    #Depth_Mid = 500
    #Width_Mid = 300 
    #Overhang_Width = 350
    #Top_Thickness = 150 
    #Dist_Top_Long = 200
    #Transverse_Length = Overhang_Width*2 + Width_Mid
    
    
    
    # ====================== Create Model ====================== 
    mdb.Model(modelType=STANDARD_EXPLICIT, name='TBEAM')


    # ====================== Create TBEAM Concrete ====================== 

    mdb.models['TBEAM'].ConstrainedSketch(name='__profile__', sheetSize=2000.0)

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        Width_Mid, 0.0))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(Width_Mid, 0.0), point2=(
        Width_Mid, Depth_Mid))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(Width_Mid, Depth_Mid), point2=
        (Overhang_Width + Width_Mid, Depth_Mid))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(Overhang_Width + Width_Mid, Depth_Mid), point2=
        (Overhang_Width + Width_Mid, Depth_Mid + Top_Thickness))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(Overhang_Width + Width_Mid, Depth_Mid + Top_Thickness), point2=
        (-Overhang_Width, Depth_Mid + Top_Thickness))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(-Overhang_Width,Depth_Mid + Top_Thickness), 
        point2=(-Overhang_Width, Depth_Mid))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(-Overhang_Width, Depth_Mid), 
        point2=(0.0, Depth_Mid))

    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(0.0, Depth_Mid), point2=(
        0.0, 0.0))

    mdb.models['TBEAM'].Part(dimensionality=THREE_D, name='TBEAM', type=
        DEFORMABLE_BODY)
    mdb.models['TBEAM'].parts['TBEAM'].BaseSolidExtrude(depth=5000.0, sketch=
        mdb.models['TBEAM'].sketches['__profile__'])
    del mdb.models['TBEAM'].sketches['__profile__']


    # ====================== Create Stirrup ====================== 

    mdb.models['TBEAM'].ConstrainedSketch(name='__profile__', sheetSize=2000.0)
    mdb.models['TBEAM'].sketches['__profile__'].rectangle(point1=(25.0, 25.0), 
        point2=(Width_Mid-25, Depth_Mid+Top_Thickness-25))
    mdb.models['TBEAM'].Part(dimensionality=THREE_D, name='STIRRUPS', type=
        DEFORMABLE_BODY)
    mdb.models['TBEAM'].parts['STIRRUPS'].BaseWire(sketch=
        mdb.models['TBEAM'].sketches['__profile__'])
    del mdb.models['TBEAM'].sketches['__profile__']
    # Save by TommyHielscher on 2022_04_12-13.43.45; build 2021 2020_03_07-01.50.37 167380



    # ====================== Create Longitudinal Rebar ====================== 
    mdb.models['TBEAM'].ConstrainedSketch(name='__profile__', sheetSize=2000.0)
    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        5000.0, 0.0))
    mdb.models['TBEAM'].Part(dimensionality=THREE_D, name='LongBar', type=
        DEFORMABLE_BODY)
    mdb.models['TBEAM'].parts['LongBar'].BaseWire(sketch=
        mdb.models['TBEAM'].sketches['__profile__'])
    del mdb.models['TBEAM'].sketches['__profile__']

        
    # ====================== Create Transverse Bar ====================== 
    mdb.models['TBEAM'].ConstrainedSketch(name='__profile__', sheetSize=2000.0)
    mdb.models['TBEAM'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        Transverse_Length, 0.0))
    mdb.models['TBEAM'].Part(dimensionality=THREE_D, name='TransvsBAR', type=
        DEFORMABLE_BODY)
    mdb.models['TBEAM'].parts['TransvsBAR'].BaseWire(sketch=
        mdb.models['TBEAM'].sketches['__profile__'])
    del mdb.models['TBEAM'].sketches['__profile__']



    # ====================== Create Material Properties ====================== 
    mdb.models['TBEAM'].Material(name='Steel')
    mdb.models['TBEAM'].materials['Steel'].Density(table=((7.8e-09, ), ))
    mdb.models['TBEAM'].materials['Steel'].Elastic(table=((210000.0, 0.3), ))
    mdb.models['TBEAM'].materials['Steel'].Plastic(table=((450.0, 0.0), ))
    mdb.models['TBEAM'].Material(name='Concrete')
    mdb.models['TBEAM'].materials['Concrete'].Density(table=((2.4e-09, ), ))
    mdb.models['TBEAM'].materials['Concrete'].Elastic(table=((15427.2973, 0.18), ))
    mdb.models['TBEAM'].materials['Concrete'].ConcreteDamagedPlasticity(table=((
        35.0, 0.1, 1.16, 0.667, 0.007985), ))
    mdb.models['TBEAM'].materials['Concrete'].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=((12.5, 0.0), (14.779363, 1.5e-05), (16.897181, 4e-05), (18.815096, 
        7.9e-05), (20.499689, 0.000132), (21.925443, 0.000202), (23.076855, 
        0.00029), (23.949385, 0.000396), (24.549184, 0.00052), (24.891777, 
        0.000661), (25.0, 0.000816), (24.901601, 0.000985), (24.626862, 0.001166), 
        (24.206509, 0.001356), (23.670071, 0.001553), (23.044731, 0.001756), (
        22.354643, 0.001964), (21.620626, 0.002174), (20.860155, 0.002386), (
        20.087539, 0.002598), (19.314226, 0.002811), (18.549152, 0.003023), (
        17.799119, 0.003235), (17.069142, 0.003445), (16.362775, 0.003653), (
        15.682397, 0.00386), (15.029454, 0.004065), (14.404665, 0.004268), (
        13.80819, 0.004469), (13.23977, 0.004669), (12.698832, 0.004866), (
        12.184584, 0.005062), (11.69608, 0.005257), (11.232271, 0.005449), (
        10.792054, 0.005641), (10.374298, 0.00583), (9.977867, 0.006019), (
        9.601643, 0.006206), (9.244531, 0.006392), (8.905476, 0.006576), (8.583462, 
        0.00676), (8.277519, 0.006942), (7.986728, 0.007124), (7.710212, 0.007304), 
        (7.5, 0.007448)))
    mdb.models['TBEAM'].materials['Concrete'].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=((3.0, 0.0), (1.664354, 0.000281), (1.179148, 0.000507), (0.923358, 
        0.000718), (0.76383, 0.000923), (0.654173, 0.001124), (0.573836, 0.001324), 
        (0.512265, 0.001522), (0.463463, 0.00172), (0.423761, 0.001917)))
    mdb.models['TBEAM'].materials['Concrete'].concreteDamagedPlasticity.ConcreteCompressionDamage(
        table=((0.0, 0.0), (0.0, 1.5e-05), (0.0, 4e-05), (0.0, 7.9e-05), (0.0, 
        0.000132), (0.0, 0.000202), (0.0, 0.00029), (0.0, 0.000396), (0.0, 
        0.00052), (0.0, 0.000661), (0.0, 0.000816), (0.003936, 0.000985), (
        0.014926, 0.001166), (0.03174, 0.001356), (0.053197, 0.001553), (0.078211, 
        0.001756), (0.105814, 0.001964), (0.135175, 0.002174), (0.165594, 
        0.002386), (0.196498, 0.002598), (0.227431, 0.002811), (0.258034, 
        0.003023), (0.288035, 0.003235), (0.317234, 0.003445), (0.345489, 
        0.003653), (0.372704, 0.00386), (0.398822, 0.004065), (0.423813, 0.004268), 
        (0.447672, 0.004469), (0.470409, 0.004669), (0.492047, 0.004866), (
        0.512617, 0.005062), (0.532157, 0.005257), (0.550709, 0.005449), (0.568318, 
        0.005641), (0.585028, 0.00583), (0.600885, 0.006019), (0.615934, 0.006206), 
        (0.630219, 0.006392), (0.643781, 0.006576), (0.656662, 0.00676), (0.668899, 
        0.006942), (0.680531, 0.007124), (0.691592, 0.007304), (0.7, 0.007448)))
    mdb.models['TBEAM'].materials['Concrete'].concreteDamagedPlasticity.ConcreteTensionDamage(
        table=((0.0, 0.0), (0.445215, 0.000281), (0.606951, 0.000507), (0.692214, 
        0.000718), (0.74539, 0.000923), (0.781942, 0.001124), (0.808721, 0.001324), 
        (0.829245, 0.001522), (0.845512, 0.00172), (0.858746, 0.001917)))
    mdb.models['TBEAM'].HomogeneousSolidSection(material='Concrete', name=
        'Concrete', thickness=None)
        
    mdb.models['TBEAM'].TrussSection(area=50.24, material='Steel', name=
        'SteelRebar')
        
    # ==================Assign Section ====================== 

    mdb.models['TBEAM'].parts['TBEAM'].Set(cells=
        mdb.models['TBEAM'].parts['TBEAM'].cells.findAt(((2, 2, 
        2), )), name='Set-1')
    mdb.models['TBEAM'].parts['TBEAM'].SectionAssignment(offset=0.0, offsetField='', 
        offsetType=MIDDLE_SURFACE, region=
        mdb.models['TBEAM'].parts['TBEAM'].sets['Set-1'], sectionName='Concrete', 
        thicknessAssignment=FROM_SECTION)
    # Save by TommyHielscher on 2022_04_12-22.02.37; build 2021 2020_03_07-01.50.37 167380


    mdb.models['TBEAM'].parts['LongBar'].Set(edges=
        mdb.models['TBEAM'].parts['LongBar'].edges.findAt(((1250.0, 0.0, 0.0), )), 
        name='Set-2')
    mdb.models['TBEAM'].parts['LongBar'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=
        mdb.models['TBEAM'].parts['LongBar'].sets['Set-2'], sectionName=
        'SteelRebar', thicknessAssignment=FROM_SECTION)
        
        
    mdb.models['TBEAM'].parts['STIRRUPS'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=mdb.models['TBEAM'].parts['STIRRUPS'].edges.findAt(((100, 25.0, 
        0.0), ), ((Width_Mid - 25, 100, 0.0), ), ((100, Depth_Mid + Top_Thickness - 25, 0.0), ), ((25.0, 100, 
        0.0), ), )), sectionName='SteelRebar', thicknessAssignment=FROM_SECTION)


    mdb.models['TBEAM'].parts['TransvsBAR'].Set(edges=
        mdb.models['TBEAM'].parts['TransvsBAR'].edges.findAt(((250.0, 0.0, 0.0), ))
        , name='Set-3')
    mdb.models['TBEAM'].parts['TransvsBAR'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['TBEAM'].parts['TransvsBAR'].sets['Set-3'], sectionName=
        'SteelRebar', thicknessAssignment=FROM_SECTION)
    # Save by TommyHielscher on 2022_04_23-14.04.26; build 2021 2020_03_07-01.50.37 167380




    #============== Start translation =============

    mdb.models['TBEAM'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['TBEAM'].rootAssembly.Instance(dependent=ON, name='LongBar-1', part=
        mdb.models['TBEAM'].parts['LongBar'])
    mdb.models['TBEAM'].rootAssembly.Instance(dependent=ON, name='STIRRUPS-1', 
        part=mdb.models['TBEAM'].parts['STIRRUPS'])
    mdb.models['TBEAM'].rootAssembly.Instance(dependent=ON, name='TBEAM-1', part=
        mdb.models['TBEAM'].parts['TBEAM'])
    mdb.models['TBEAM'].rootAssembly.Instance(dependent=ON, name='TransvsBAR-1', 
        part=mdb.models['TBEAM'].parts['TransvsBAR'])


    #==============Rotate and move Long rebar================#
    mdb.models['TBEAM'].rootAssembly.rotate(angle=270.0, axisDirection=(0.0, 
        716.7944, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('LongBar-1', ))
    mdb.models['TBEAM'].rootAssembly.translate(instanceList=('LongBar-1', ), 
        vector=(25.0, 25.0, 0.0))
        
        
    #==============Rotate and move Transverse============#
    mdb.models['TBEAM'].rootAssembly.translate(instanceList=('TransvsBAR-1', ), 
        vector=( -Overhang_Width, Depth_Mid + Top_Thickness - 25, 0.0))

        


        
    # ====================== Copy to create pattern (Longitudinal Rebar) ====================== 
    mdb.models['TBEAM'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 
        0.0), direction2=(0.0, 1.0, 0.0), instanceList=('LongBar-1', ), number1=3, 
        number2=2, spacing1=(Width_Mid-50)/2, spacing2= Depth_Mid + Top_Thickness - 50)

    # ====================== Copy to create pattern (Stirrups) ====================== 
    mdb.models['TBEAM'].rootAssembly.LinearInstancePattern(direction1=(0.0, 0.0, 
        1.0), direction2=(0.0, 1.0, 0.0), instanceList=('STIRRUPS-1', ), number1=26
        , number2=1, spacing1=200.0, spacing2=600.0)
    # ====================== Copy to create pattern (Transverse bars)====================== 
    mdb.models['TBEAM'].rootAssembly.LinearInstancePattern(direction1=(0.0, 0.0, 
        1.0), direction2=(0.0, 1.0, 0.0), instanceList=('TransvsBAR-1', ), number1=
        26, number2=1, spacing1=200.0, spacing2=1.0)
        
    # ====================== Copy to create pattern (LongBar)======== 
    mdb.models['TBEAM'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 
        0.0), direction2=(0.0, 1.0, 0.0), instanceList=('LongBar-1-lin-3-2', ), 
        number1=2, number2=1, spacing1=Dist_Top_Long, spacing2=1.0)
        
    # ====================== Copy to create pattern (additional longitudinal rebar) ====================== 
    mdb.models['TBEAM'].rootAssembly.LinearInstancePattern(direction1=(-1, 0.0, 
        0.0), direction2=(0.0, 1.0, 0.0), instanceList=('LongBar-1-lin-1-2', ), 
        number1=2, number2=1, spacing1=Dist_Top_Long, spacing2=1.0)
    # Save by TommyHielscher on 2022_04_12-14.37.03; build 2021 2020_03_07-01.50.37 167380


    #======================== Set Boundary Condition A =================================
    mdb.models['TBEAM'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
        distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
        region=Region(
        faces=mdb.models['TBEAM'].rootAssembly.instances['TBEAM-1'].faces.findAt(((
        2, 2, 0.0), ), ((4, 4, 0.0), ), )), 
        u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    # Save by TommyHielscher on 2022_04_12-23.18.02; build 2021 2020_03_07-01.50.37 167380

    #======================== Set Boundary Condition B ================================
    mdb.models['TBEAM'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
        distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
        region=Region(
        faces=mdb.models['TBEAM'].rootAssembly.instances['TBEAM-1'].faces.findAt(((
        2, 2, 5000.0), ), ((4, 4, 5000.0), ), 
        )), u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    # Save by TommyHielscher on 2022_04_12-23.16.00; build 2021 2020_03_07-01.50.37 167380


    # ====================== Create Mesh ====================== 

    mdb.models['TBEAM'].parts['LongBar'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=50.0)
    mdb.models['TBEAM'].parts['LongBar'].generateMesh()
    mdb.models['TBEAM'].parts['STIRRUPS'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=50.0)
    mdb.models['TBEAM'].parts['STIRRUPS'].generateMesh()
    mdb.models['TBEAM'].parts['TBEAM'].seedPart(deviationFactor=0.1, minSizeFactor=
        0.1, size=25.0)
    mdb.models['TBEAM'].parts['TBEAM'].generateMesh()
    mdb.models['TBEAM'].parts['TransvsBAR'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=50.0)
    mdb.models['TBEAM'].parts['TransvsBAR'].generateMesh()
    # Save by TommyHielscher on 2022_04_12-15.11.59; build 2021 2020_03_07-01.50.37 167380


    #################################

    # ====================== Set Element Type ====================== 

    mdb.models['TBEAM'].parts['TransvsBAR'].setElementType(elemTypes=(ElemType(
        elemCode=T3D2, elemLibrary=STANDARD), ), regions=(
        mdb.models['TBEAM'].parts['TransvsBAR'].edges.findAt(((250.0, 0.0, 0.0), 
        )), ))
    mdb.models['TBEAM'].parts['STIRRUPS'].setElementType(elemTypes=(ElemType(
        elemCode=T3D2, elemLibrary=STANDARD), ), regions=(
        mdb.models['TBEAM'].parts['STIRRUPS'].edges.findAt(((50, 25.0, 0.0), ), 
        ((Width_Mid - 25, 100, 0.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 0.0), ), ((25.0, 175.0, 0.0), ), ), 
        ))
    mdb.models['TBEAM'].parts['LongBar'].setElementType(elemTypes=(ElemType(
        elemCode=T3D2, elemLibrary=STANDARD), ), regions=(
        mdb.models['TBEAM'].parts['LongBar'].edges.findAt(((1250.0, 0.0, 0.0), )), 
        ))
    mdb.models['TBEAM'].parts['TBEAM'].setElementType(elemTypes=(ElemType(
        elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
        kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT, 
        distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
        ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
        mdb.models['TBEAM'].parts['TBEAM'].cells.findAt(((-50.0, Depth_Mid + 50, 
        3333.333333), )), ))
    # Save by TommyHielscher on 2022_04_23-14.07.47; build 2021 2020_03_07-01.50.37 167380


    # ===================== Set Constraints ================
    mdb.models['TBEAM'].rootAssembly.Set(edges=
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1'].edges.findAt(((
        25.0, 25.0, 1250.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1'].edges.findAt(((
        100, 25.0, 0.0), ), ((Width_Mid- 25, 100, 0.0), ), ((100, Depth_Mid + Top_Thickness - 25, 0.0), ), ((
        25.0, 100, 0.0), ), )+\
        
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1'].edges.findAt(((
        -100.0, Depth_Mid + Top_Thickness - 25, 0.0), ), )+\
        
        
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-1-2'].edges.findAt(
        ((25.0, Depth_Mid + Top_Thickness - 25, 1250.0), ), )+\
        
        #This is working
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-2-1'].edges.findAt(
        ((Width_Mid/2, 25.0, 1250.0), ), )+\
        
        #This is working
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-2-2'].edges.findAt(
        ((Width_Mid/2, Depth_Mid + Top_Thickness - 25, 1250.0), ), )+\
        
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-3-1'].edges.findAt(
        ((Width_Mid - 25, 25.0, 1250.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-3-2'].edges.findAt(
        ((Width_Mid - 25, Depth_Mid + Top_Thickness - 25, 1250.0), ), )+\
        
        # External Long rebar
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-3-2-lin-2-1'].edges.findAt(
        ((Dist_Top_Long + Width_Mid - 25, Depth_Mid + Top_Thickness - 25, 1250.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['LongBar-1-lin-1-2-lin-2-1'].edges.findAt(
        ((-Dist_Top_Long + 25, Depth_Mid + Top_Thickness - 25, 1250.0), ), )+\
        #
        
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-2-1'].edges.findAt(
        ((100, 25.0, 200.0), ), ((Width_Mid - 25, 100, 200.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 200.0), 
        ), ((25.0, 175.0, 200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-3-1'].edges.findAt(
        ((50, 25.0, 400.0), ), ((Width_Mid - 25, 100, 400.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 400.0), 
        ), ((25.0, 175.0, 400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-4-1'].edges.findAt(
        ((50, 25.0, 600.0), ), ((Width_Mid - 25, 100, 600.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 600.0), 
        ), ((25.0, 175.0, 600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-5-1'].edges.findAt(
        ((50, 25.0, 800.0), ), ((Width_Mid - 25, 100, 800.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 800.0), 
        ), ((25.0, 175.0, 800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-6-1'].edges.findAt(
        ((50, 25.0, 1000.0), ), ((Width_Mid - 25, 100, 1000.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        1000.0), ), ((25.0, 175.0, 1000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-7-1'].edges.findAt(
        ((50, 25.0, 1200.0), ), ((Width_Mid - 25, 100, 1200.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        1200.0), ), ((25.0, 175.0, 1200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-8-1'].edges.findAt(
        ((50, 25.0, 1400.0), ), ((Width_Mid - 25, 100, 1400.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        1400.0), ), ((25.0, 175.0, 1400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-9-1'].edges.findAt(
        ((50, 25.0, 1600.0), ), ((Width_Mid - 25, 100, 1600.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        1600.0), ), ((25.0, 175.0, 1600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-10-1'].edges.findAt(
        ((50, 25.0, 1800.0), ), ((Width_Mid - 25, 100, 1800.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        1800.0), ), ((25.0, 175.0, 1800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-11-1'].edges.findAt(
        ((50, 25.0, 2000.0), ), ((Width_Mid - 25, 100, 2000.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        2000.0), ), ((25.0, 175.0, 2000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-12-1'].edges.findAt(
        ((50, 25.0, 2200.0), ), ((Width_Mid - 25, 100, 2200.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        2200.0), ), ((25.0, 175.0, 2200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-13-1'].edges.findAt(
        ((50, 25.0, 2400.0), ), ((Width_Mid - 25, 100, 2400.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        2400.0), ), ((25.0, 175.0, 2400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-14-1'].edges.findAt(
        ((50, 25.0, 2600.0), ), ((Width_Mid - 25, 100, 2600.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        2600.0), ), ((25.0, 175.0, 2600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-15-1'].edges.findAt(
        ((50, 25.0, 2800.0), ), ((Width_Mid - 25, 100, 2800.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        2800.0), ), ((25.0, 175.0, 2800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-16-1'].edges.findAt(
        ((50, 25.0, 3000.0), ), ((Width_Mid - 25, 100, 3000.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        3000.0), ), ((25.0, 175.0, 3000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-17-1'].edges.findAt(
        ((50, 25.0, 3200.0), ), ((Width_Mid - 25, 100, 3200.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        3200.0), ), ((25.0, 175.0, 3200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-18-1'].edges.findAt(
        ((50, 25.0, 3400.0), ), ((Width_Mid - 25, 100, 3400.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        3400.0), ), ((25.0, 175.0, 3400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-19-1'].edges.findAt(
        ((50, 25.0, 3600.0), ), ((Width_Mid - 25, 100, 3600.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        3600.0), ), ((25.0, 175.0, 3600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-20-1'].edges.findAt(
        ((50, 25.0, 3800.0), ), ((Width_Mid - 25, 100, 3800.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        3800.0), ), ((25.0, 175.0, 3800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-21-1'].edges.findAt(
        ((50, 25.0, 4000.0), ), ((Width_Mid - 25, 100, 4000.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        4000.0), ), ((25.0, 175.0, 4000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-22-1'].edges.findAt(
        ((50, 25.0, 4200.0), ), ((Width_Mid - 25, 100, 4200.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        4200.0), ), ((25.0, 175.0, 4200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-23-1'].edges.findAt(
        ((50, 25.0, 4400.0), ), ((Width_Mid - 25, 100, 4400.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        4400.0), ), ((25.0, 175.0, 4400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-24-1'].edges.findAt(
        ((50, 25.0, 4600.0), ), ((Width_Mid - 25, 100, 4600.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        4600.0), ), ((25.0, 175.0, 4600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-25-1'].edges.findAt(
        ((50, 25.0, 4800.0), ), ((Width_Mid - 25, 100, 4800.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        4800.0), ), ((25.0, 175.0, 4800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['STIRRUPS-1-lin-26-1'].edges.findAt(
        ((50, 25.0, 5000.0), ), ((Width_Mid - 25, 100, 5000.0), ), ((87.5, Depth_Mid + Top_Thickness - 25, 
        5000.0), ), ((25.0, 175.0, 5000.0), ), )+\
        
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-2-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-3-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-4-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-5-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-6-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 1000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-7-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 1200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-8-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 1400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-9-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 1600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-10-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 1800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-11-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 2000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-12-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 2200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-13-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 2400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-14-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 2600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-15-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 2800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-16-1'].edges.findAt(
        ((-100.0,Depth_Mid + Top_Thickness - 25, 3000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-17-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 3200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-18-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 3400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-19-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 3600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-20-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 3800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-21-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 4000.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-22-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 4200.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-23-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 4400.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-24-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 4600.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-25-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 4800.0), ), )+\
        mdb.models['TBEAM'].rootAssembly.instances['TransvsBAR-1-lin-26-1'].edges.findAt(
        ((-100.0, Depth_Mid + Top_Thickness - 25, 5000.0), ), ), name='m_Set-3')
    mdb.models['TBEAM'].rootAssembly.Set(cells=
        mdb.models['TBEAM'].rootAssembly.instances['TBEAM-1'].cells.findAt(((
        -Overhang_Width, Depth_Mid + 50, 3333.333333), )), name='s_Set-3')
        
        
    mdb.models['TBEAM'].EmbeddedRegion(absoluteTolerance=0.0, embeddedRegion=
        mdb.models['TBEAM'].rootAssembly.sets['m_Set-3'], fractionalTolerance=0.05, 
        hostRegion=mdb.models['TBEAM'].rootAssembly.sets['s_Set-3'], name=
        'Constraint-1', toleranceMethod=BOTH, weightFactorTolerance=1e-06)
    # Save by TommyHielscher on 2022_04_23-12.25.38; build 2021 2020_03_07-01.50.37 167380




    # ====================== Create Step ====================== 
    mdb.models['TBEAM'].StaticStep(name='Step-1', previous='Initial')
    # ====================== Apply Pressure ====================== 
    mdb.models['TBEAM'].rootAssembly.Surface(name='Surf-1', side1Faces=
        mdb.models['TBEAM'].rootAssembly.instances['TBEAM-1'].faces.findAt(((
        0, Depth_Mid + Top_Thickness, 10), )))
    mdb.models['TBEAM'].Pressure(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, field='', magnitude=10.0e-6, name='Load-1', region=
        mdb.models['TBEAM'].rootAssembly.surfaces['Surf-1'])
    # Save by TommyHielscher on 2022_04_23-12.12.52; build 2021 2020_03_07-01.50.37 167380



    # ====================== Create Job ====================== 

    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='TBEAM', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name='TBEAM', nodalOutputPrecision=SINGLE, 
        numCpus=4, numDomains=4, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
        '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    # Save by TommyHielscher on 2022_04_12-15.08.22; build 2021 2020_03_07-01.50.37 167380


    # ====================== Submit Job ====================== 


    #mdb.jobs['TBEAM'].submit(consistencyChecking=OFF)
    myJob1 = mdb.Job(name='TBEAM', model='TBEAM',)
    myJob1.submit()
    # Wait for the Job to complete. 
    try:
        myJob1.waitForCompletion(6000)
    except AbaqusException, message:
        print "Job timed out", message


    # ====================== Collect Results ====================== TESTING

    from abaqus import *
    from abaqusConstants import *
    session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=290, 
        height=160)
    session.viewports['Viewport: 1'].makeCurrent()
    session.viewports['Viewport: 1'].maximize()
    from caeModules import *
    from driverUtils import executeOnCaeStartup

    img_folder = 'Images/'
    txt_folder = 'Output/'

    o1 = session.openOdb(
        name='C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/TBEAM.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)

    # Set Camera for deflection image capture
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
        visibleEdges=FEATURE)
    session.printOptions.setValues(vpDecorations=OFF)
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT, 
        'Magnitude'), )
    session.printToFile(fileName=img_folder+'IsoImage_' + str(sol), format=TIFF, canvasObjects=(
        session.viewports['Viewport: 1'], ))

    # This is currently only looking at one point

    # Export data to text file
    session.xyDataListFromField(odb=o1, outputPosition=NODAL, variable=(('U', 
        NODAL, ((INVARIANT, 'Magnitude'), )), ), nodePick=(('TBEAM-1', 1, (
        '[#0:1944 #10000000 ]', )), ), )
    xy1 = session.xyDataObjects['U:Magnitude PI: TBEAM-1 N: 62237']
    session.writeXYReport(fileName=txt_folder+'abaqus_output_' + str(sol) +'.txt', appendMode=OFF, xyData=(xy1, 
        ))
    del session.xyDataObjects['U:Magnitude PI: TBEAM-1 N: 62237']
    # END OF TESTING
    # ====================== Close the file ====================== 
    mdb.close()
    
    # ====================== Checking to end script ====================== 
      
    if sol < iterations:
        sol += 1
        print("Going on to next solution")
        continue
    
    print("End of Analysis")
    break