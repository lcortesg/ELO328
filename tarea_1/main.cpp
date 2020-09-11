/*
 * @brief: Tarea 1.
 * @author: Lucas Cortés G., Aline Covarrubias G., Mathias Sanhueza L., Christian Pflaumer A.
 * @date: 2020/09/11
 * @compiler: g++ $(pkg-config --cflags --libs opencv4) -std=c++11 main.cpp -o GAMMA
 */

#include <stdio.h>
#include <math.h> 
#include <time.h>
#include <chrono> 
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;
using namespace chrono; 

// Variables globales.
const int borde = 50; // Ancho del borde.
bool invertir = false; // Invierte la imagen horizontalmente.
bool timer = true; // Muestra el timer.
bool tabla = false, pixel = false, imagen = false, video = false; // Tipo de procesamiento a realizar.
int R = 0, G = 0, B = 0, X = 0, Y = 0, W, H; // Color borde, posición, ancho y alto de ventana.
float gamma_value; // Valor de corrección Gamma.
cv::Mat img, img_out, img_border; // Matrices de imágenes.

void corregir_tabla(Mat& img, float gamma_value){ // Función de corrección por tabla.
	unsigned char gamma_table[256]; // Creación de la tabla Gamma.
	for (int i = 0; i < 256; i++) gamma_table[i] = saturate_cast<uchar>(pow((float)(i / 255.0), gamma_value) * 255.0f);
	MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = gamma_table[(*it)];
} 

void corregir_pixel(Mat& img, float gamma_value){ // Función de correción pixel a pixel.
	MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = saturate_cast<uchar>(pow((float)(*it/255.0), gamma_value) * 255.0f);
}

void corregir(){
    cv::cvtColor(img, img_out, cv::COLOR_BGR2YCrCb); // Se convierte la imagen desde BGR a YUV.
    cv::Mat whole = img_out; // Imagen en YUV.
	cv::Mat img_part(
	whole,
	cv::Range( Y, Y+H ), // rows.
	cv::Range( X, X+W ));// cols.
	
	auto start = high_resolution_clock::now();// Se inicia el timer.
	if (tabla) corregir_tabla(img_part, gamma_value);// Corrección Gamma con tabla.
    if (pixel) corregir_pixel(img_part, gamma_value); // Corrección Gamma con función.
	auto stop = high_resolution_clock::now(); // Se detiene el timer.
	auto duration = duration_cast<microseconds>(stop - start); // Se calcula la duración del timer.
	if(timer) cout<<"Tiempo de conversión de imagen: "<<duration.count()<<" microsegundos"<< endl;

	cv::cvtColor(img_part, img_part, cv::COLOR_YCrCb2BGR);// Se convierte la imagen desde color YUB a BGR.
	img_part.copyTo(img(cv::Rect(X, Y, img_part.cols, img_part.rows))); // Se fusiona la ventana corregida.
	Scalar value(B,G,R); // Se genera vector de valores BGR;
	copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value); // Se genera el borde.
	cv::imshow("Imagen con correcion Gamma en capa de luminancia", img_border); // Se muestra la imagen corregida.
}


int main(int argc, char *argv[]){

    if ((argv[2][1])==105 || (argv[2][1])==73){ // Encuentra el valor "i" en el segundo argumento.
	    if(argc < 5 || argc > 14) { // Mensaje de error en caso de usar menos de 4 argumentos o más de 13.
	        cerr << "Usage: ./GAMMA [-m1 | -m2] -i image gamma [-f x y w h] [-c r g b]" << endl;
	        return 1;
	    }
	    imagen = true;
	    gamma_value = atof(argv[4]); // Guarda el valor de Gamma.
    	cout<<"Procesamiento de imagen nivel gamma: "<<gamma_value;
    }
    
    if ((argv[2][1])==118 || (argv[2][1])==86){ // Encuentra el valor "v" en el segundo argumento.
    	
	    if(argc < 4 || argc > 13) { // Mensaje de error en caso de usar menos de 3 argumentos o más de 12.
	        cerr << "Usage: ./GAMMA [-m1 | -m2] -v gamma [-f x y w h] [-c r g b]" << endl;
	        return 1;
	    }
    	video = true;
    	gamma_value = atof(argv[3]); // Guarda el valor de Gamma.
    	cout<<"Procesamiento de video nivel gamma: "<<gamma_value;
    }
    
    if ((argv[1][2])==49){ // Encuentra el valor "-m1" en el primer argumento.
    	tabla = true;
		cout<<" calculado por tabla."<<endl;
	}

    if ((argv[1][2])==50){ // Encuentra el valor "-m2" en el primer argumento.
    	pixel = true;
    	cout<<"calculado pixel a pixel."<<endl;
    }
    
    if (imagen){ // Lógica de procesamiento de imagen.
        
    	img = cv::imread(argv[3], 1); // Lee la imagen
        W = img.cols;
        H = img.rows;
        
	    if(img.empty()){ // Si no se encuentra la imagen. 
	        cerr << "Error leyendo imagen " << argv[3] << endl;
	        return 1;
	    }

        if(argc>=9){ // Definiciones de borde y ventana.

        	if (argc==9 && ((argv[5][1])==99 || (argv[5][1])==67)){ // c ó C
        		R = atof(argv[6]);
        		G = atof(argv[7]);
                B = atof(argv[8]);  
            }

            if (argc==10 && ((argv[5][1])==102 || (argv[5][1])==70)){ // f ó F
                X = atof(argv[6]);
                Y = atof(argv[7]);
                W = (atof(argv[8]) != 0) ? atof(argv[8]) : 1;
                H = (atof(argv[9]) != 0) ? atof(argv[9]) : 1;
            }

            if (argc>10 && ((argv[10][1])==99 || (argv[10][1])==67)){ // c ó C
            	X = atof(argv[6]);
                Y = atof(argv[7]);
                W = (atof(argv[8]) != 0) ? atof(argv[8]) : 1;
                H = (atof(argv[9]) != 0) ? atof(argv[9]) : 1;
                R = atof(argv[11]);
                G = atof(argv[12]);
                B = atof(argv[13]);
            }

            if (X+W > img.cols || Y+H > img.rows){ // Error si la ventana excede las dimensiones de la imagen.
            	cerr << "Las dimensiones (X+W)*(Y+H): "<<X+W<<"x"<<Y+H<<" superan a las de la imagen: "<<img.cols<<"x"<<img.rows<<"."<<endl;
        		return 1;
            }   
        }
        cout << "Se inicia la conversion" << endl << "Presionar cualquier tecla para salir" << endl;
        corregir();// Se corrige la imagen.
    }
        
    if (video){ // Lógica de procesamiento de video.

        VideoCapture cap; // Captura de video.
        //cap.open(0); // Abre la cámara default usando la API por default.
        int deviceID = 0; // 0 = Cámara por default.
        int apiID = cv::CAP_ANY; // 0 = Autodetectar API por default.
        cap.open(deviceID, apiID); // Abrir la cámara seleccionada usando la API seleccionada.
        
        if (!cap.isOpened()) { // Revisar si no hay errores
            cerr << "Error abriendo camara\n";
            return -1;
        }
        
        cout << "Se inicia la grabacion" << endl << "Presionar cualquier tecla para salir" << endl;

        for (;;){ // Loop de captura.

            cap.read(img); // Esperar por un nuevo frame.
            if(invertir) cv::flip(img, img, 1); // Invierte la imagen horizontalmente.
            W = img.cols;
        	H = img.rows;

            if (img.empty()){ // Revisar si no hay errores.
                cerr << "Frame en blanco\n";
                break;
            }

            else if(argc>=8){ // Definiciones de borde y ventana.

            	if (argc==8 && ((argv[4][1])==99 || (argv[4][1])==67)){ // c ó C
                    R = atof(argv[5]);
                    G = atof(argv[6]);
                    B = atof(argv[7]);
                }

                if (argc==9 && ((argv[4][1])==102 || (argv[4][1])==70)){ // f ó F
                    X = atof(argv[5]);
                    Y = atof(argv[6]);
                    W = (atof(argv[7]) != 0) ? atof(argv[7]) : 1;
                	H = (atof(argv[8]) != 0) ? atof(argv[8]) : 1;
                }  

                if (argc>9 && ((argv[9][1])==99 || (argv[9][1])==67)){ // c ó C
                	X = atof(argv[5]);
                    Y = atof(argv[6]);
                    W = (atof(argv[7]) != 0) ? atof(argv[7]) : 1;
                	H = (atof(argv[8]) != 0) ? atof(argv[8]) : 1;
                    R = atof(argv[10]);
                    G = atof(argv[11]);
                    B = atof(argv[12]);
                }

                if (X+W > img.cols || Y+H > img.rows){ // Error si la ventana excede las dimensiones de la imagen.
            		cerr << "Las dimensiones (X+W)*(Y+H): "<<X+W<<"x"<<Y+H<<" superan a las de la imagen: "<<img.cols<<"x"<<img.rows<<"."<<endl;
        			return 1;
            	}
            }
            corregir(); // Se corrige la imagen.
            if (waitKey(5) >= 0) break;
        }
        return 0;
    }
    waitKey(0);
    return 0;
}


