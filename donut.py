import math

#To draw a circle on 2D, plot the points for each change in theta {0..2pi} according to the equation (R1 cos theta, R1 sin theta, 0) to get (x, y, z)
#Theta value change
thetaSpacing = 0.07
#To rotate a circle about y-axis, multiple it by a rotation matrix along phi
#Phi value change
phiSpacing = 0.02
#Radius of torus from center point to inner circle
R1 = 1
#Radius of torus from center point to outer circle
R2 = 2

#Distance of donut from viewer
K2 = 5

#Refers to z' which is distance of eye to screen
#Controls the scale, depends on pixel resolution
screenW = 35
K1 = screenW*K2*3/(8*(R1+R2))
screenH = 35

#method
def rendering(A, B):
    #Compute sine and cosines of A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)
    
    charOutput = [] #fills the circle with characters 
    zList = [] #z co-ords for all pixels
    
    #initialise donut char and zbuffer w/ zeros & spaces
    for i in range(screenH + 1):
        charOutput.append([' '] * (screenW + 0))
        zList.append([0] * (screenW + 0))
    
    #theta goes from 0 to 2pi, draws 2D circle
    theta = 0
    while (theta < 2* math.pi):
        #Increment theta by theta_spacing to get next point, increments until full circle (2*mathpi)
        theta += thetaSpacing
        #Compute sine and cosines theta
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
       
        #circle rotates on y-axis, phi 0 to 2pi, while metho
        phi = 0
        while (phi < 2*math.pi):
            #same maths as above for y/phi
            phi += phiSpacing
            #Compute sine and cosines phi
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            #rotation time
            #co-ords before rotation x*y respectively
            circlex = R2 + R1*costheta
            circley = R1*sintheta
            #co-ords after rotation 3D, got help for this equ
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA
            depth = 1/z #pix depth
            
            #illustration of x and y
            xp = int(screenW/2 + K1*depth*x)
            yp = int(screenH/2 - K1*depth*y)

            #this was confusing
            #matrix multiplication to calc luminance of the pixs
            #screen light surface normal * light source from back of donut
            #in this case it was lum = (Nx, Ny, Nz)*(0, 1, -1) 
            lum = (
                    cosphi*costheta*sinB
                    - cosA*costheta*sinphi 
                    - sinA*sintheta 
                    + cosB*(cosA*sintheta - costheta*sinA*sinphi)
            )
            
            #more luminance fun
            #so lum ranges -sqrt(2) to +srt(2)
            #if lum is less than 0 then surface is pointing away and we dont want to plot that 
            if lum > 0:
                #if 1/z (depth) is larger than z, pixel closer to us than plotted
                if depth > zList[xp][yp]:
                    zList[xp][yp] = depth
                    #luminance_index is mult so to be in the range 0..11 (8*sqrt(2) = 11.3)
                    #(i think to make lum indx bigger i.e donut more prominant/bigger/luminous)
                    luminance_index = lum*8
                    #look and store char related to lum 
                    charOutput[xp][yp] = '.,-~:;=!*#$@'[int(luminance_index)]
    
    #clear screen and dump charOutput[] to screen
    print('\x1b[H')
    for i in range(screenH):
        for j in range(screenW):
            print(charOutput[i][j], end='')
        print()



print('\x1b[2J')
A = 1.0
B = 1.0

# For how many frames do you want this to loop
for i in range(250):
    rendering(A, B)
    #Rate of change in angle of rotation in one axis(delta val), then incremented by delta val
    A += 0.0
    # Rate of change in angle of rotation in one axis, in opposite direction of A(delta val), then incremented by delta val
    B += 0.03

#Protects accidental invocations i.e unguarded imported into other scripts running with cmd line args from this donut
if __name__ == '__main__':
    main()