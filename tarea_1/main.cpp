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
// Ancho del borde.
const int borde = 50; 
// Muestra el timer.
bool timer = true;
// Valores booleanos que determinan el tipo de procesamiento a realizar.
bool tabla = false, pixel = false, imagen = false, video = false;
// Valores de color de borde, posición, ancho y alto de la ventana rectangular a procesar.
int R = 0, G = 0, B = 0, X = 0, Y = 0, W, H;
// Valor de corrección Gamma.
float gamma_value;
// Matrices de imágenes.
cv::Mat img, img_out, img_border;


// Función de corrección por tabla.
void corregir_tabla(Mat& img, float gamma_value){

	unsigned char gamma_table[256];

	// Creación de la tabla Gamma
	for (int i = 0; i < 256; i++) gamma_table[i] = saturate_cast<uchar>(pow((float)(i / 255.0), gamma_value) * 255.0f);
	
	MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = gamma_table[(*it)];
} 


// Función de correción pixel a pixel.
void corregir_pixel(Mat& img, float gamma_value){

	MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = saturate_cast<uchar>(pow((float)(*it/255.0), gamma_value) * 255.0f);
}

void corregir(){

	// Se convierte la imagen de espacio de color BGR a YUV.
    cv::cvtColor(img, img_out, cv::COLOR_BGR2YCrCb);
 	
 	// Se recorta el rectángulo a modificar.
    cv::Mat whole = img_out; // Imagen en YUV.
	cv::Mat img_part(
	whole,
	cv::Range( Y, Y+H ), // rows.
	cv::Range( X, X+W ));// cols.
	
	// Se inicia el timer	
	auto start = high_resolution_clock::now();

	// Corrección Gamma con tabla.
	if (tabla) corregir_tabla(img_part, gamma_value);

	// Corrección Gamma con función.
    if (pixel) corregir_pixel(img_part, gamma_value); 

    // Se detiene el timer.
	auto stop = high_resolution_clock::now(); 
	auto duration = duration_cast<microseconds>(stop - start);
	if(timer) cout<<"Tiempo de conversión de imagen: "<<duration.count()<<" microsegundos"<< endl;

	// Se convierte la imagen de espacio de color YUB a BGR.
	cv::cvtColor(img_part, img_part, cv::COLOR_YCrCb2BGR);
	//cv::cvtColor(img_part, img_part, cv::COLOR_BGR2HLS);
	img_part.copyTo(img(cv::Rect(X, Y, img_part.cols, img_part.rows)));

	// Se genera el borde.
	Scalar value(R,G,B);
	copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);

	// Se muestra la imagen corregida.
	cv::imshow("Imagen con correcion Gamma en capa de luminancia", img_border);
}


int main(int argc, char *argv[]){
	
    // Encuentra el valor "i" en el segundo argumento.
    if ((argv[2][1])==105 || (argv[2][1])==73){
    	// Muestra mensaje error en caso de utilizar menos de 4 argumentos o más de 13.
	    if(argc < 5 || argc > 14) {
	        cerr << "Usage: ./GAMMA [-m1 | -m2] -i image gamma [-f x y w h] [-c r g b]" << endl;
	        return 1;
	    }
	    imagen = true;
	    // Guarda el valor de Gamma
	    gamma_value = atof(argv[4]);
    	cout<<"Procesamiento de imagen nivel gamma : "<<gamma_value;
    }

    // Encuentra el valor "v" en el segundo argumento.
    if ((argv[2][1])==118 || (argv[2][1])==86){
    	// Muestra mensaje error en caso de utilizar menos de 3 argumentos o más de 12.
	    if(argc < 4 || argc > 13) {
	        cerr << "Usage: ./GAMMA [-m1 | -m2] -v gamma [-f x y w h] [-c r g b]" << endl;
	        return 1;
	    }
    	video = true;
    	// Guarda el valor de Gamma
    	gamma_value = atof(argv[3]);
    	cout<<"Procesamiento de video nivel gamma : "<<gamma_value;
    }

    // Encuentra el valor "-m1" en el primer argumento.
    if ((argv[1][2])==49){
    	tabla = true;
		cout<<" calculado por tabla."<<endl;
	}

    // Encuentra el valor "-m2" en el primer argumento.
    if ((argv[1][2])==50){
    	pixel = true;
    	cout<<"calculado pixel a pixel."<<endl;
    }

    // Lógica de procesamiento de imagen.
    if (imagen){

        // Lee la imagen
    	img = cv::imread(argv[3], 1);
        W = img.cols;
        H = img.rows;

        // Si no se encuentra la imagen. 
	    if(img.empty()) {
	        cerr << "Error leyendo imagen " << argv[3] << endl;
	        return 1;
	    }

	    // Definiciones de borde y rectángulo
        if(argc>=9){

        	if (argc==9 && ((argv[5][1])==99 || (argv[5][1])==67)){ // c ó C
        		B = atof(argv[6]);
        		G = atof(argv[7]);
                R = atof(argv[8]);  
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
                B = atof(argv[11]);
                G = atof(argv[12]);
                R = atof(argv[13]);
            }

            if (X+W > img.cols || Y+H > img.rows){
            	cerr << "Las dimensiones (X+W)*(Y+H)= "<<X+W<<"x"<<Y+H<<" superan a las de la imagen: "<<img.cols<<"x"<<img.rows<<"."<<endl;
        		return 1;
            }   
        }

        cout << "Se inicia la conversion" << endl
        << "Presionar cualquier tecla para salir" << endl;

        // Se corrige la imagen.
        corregir();
    }
        
    // Lógica de procesamiento de video.
    if (video){

        Mat frame;
       
        // Captura de video.
        VideoCapture cap;
        // Abre la cámara default usando la API por default.
        // cap.open(0);
        int deviceID = 0;             // 0 = Cámara por default.
        int apiID = cv::CAP_ANY;      // 0 = Autodetectar API por default.
        // Abrir la cámara seleccionada usando la API seleccionada.
        cap.open(deviceID, apiID);

        // Revisar si no hay errores
        if (!cap.isOpened()) {
            cerr << "Error abriendo camara\n";
            return -1;
        }
        
        // Loop de captura.
        cout << "Se inicia la grabacion" << endl
        << "Presionar cualquier tecla para salir" << endl;

        for (;;){

            // Esperar por u nuevo frame.
            cap.read(frame);
            W = frame.cols;
        	H = frame.rows;

            // Revisar si no hay errores.
            if (frame.empty()) {
                cerr << "Frame en blanco\n";
                break;
            }

            // Definiciones de borde y rectángulo
            else if(argc>=8){ 

            	if (argc==8 && ((argv[4][1])==99 || (argv[4][1])==67)){ // c ó C
                    R = atof(argv[7]);
                    G = atof(argv[6]);
                    B = atof(argv[5]);
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
                    R = atof(argv[12]);
                    G = atof(argv[11]);
                    B = atof(argv[10]);
                }

                if (X+W > frame.cols || Y+H > frame.rows){
            		cerr << "Las dimensiones (X+W)*(Y+H)= "<<X+W<<"x"<<Y+H<<" superan a las de la imagen: "<<frame.cols<<"x"<<frame.rows<<"."<<endl;
        			return 1;
            	}
            }

            // Se clona el frame de video en "img"
            img = frame.clone();

            // Se corrige la imagen.
            corregir();

            if (waitKey(5) >= 0)
                break;  
        }
        return 0;
    }
    waitKey(0);
    return 0;
}






