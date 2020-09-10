// Opciones de compilación y ejecución
// g++ $(pkg-config --cflags --libs opencv4) -std=c++11 main.cpp -o GAMMA
// ./GAMMA [-m1 | -m2] -i image gamma [-f x y w h] [-c r g b]
// ./GAMMA [-m1 | -m2] -v gamma [-f x y w h] [-c r g b]

#include <stdio.h>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

const int borde = 50;
// Tabla para Gamma 0.5
const uint8_t gamma_lutp5[256] = {
     0,  16,  23,  28,  32,  36,  39,  42,  45,  48,  50,  53,  55,  58,  60,  62,
    64,  66,  68,  70,  71,  73,  75,  77,  78,  80,  81,  83,  84,  86,  87,  89,
    90,  92,  93,  94,  96,  97,  98, 100, 101, 102, 103, 105, 106, 107, 108, 109,
   111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126, 127,
   128, 129, 130, 131, 132, 133, 134, 135, 135, 136, 137, 138, 139, 140, 141, 142,
   143, 144, 145, 145, 146, 147, 148, 149, 150, 151, 151, 152, 153, 154, 155, 156,
   156, 157, 158, 159, 160, 160, 161, 162, 163, 164, 164, 165, 166, 167, 167, 168,
   169, 170, 170, 171, 172, 173, 173, 174, 175, 176, 176, 177, 178, 179, 179, 180,
   181, 181, 182, 183, 183, 184, 185, 186, 186, 187, 188, 188, 189, 190, 190, 191,
   192, 192, 193, 194, 194, 195, 196, 196, 197, 198, 198, 199, 199, 200, 201, 201,
   202, 203, 203, 204, 204, 205, 206, 206, 207, 208, 208, 209, 209, 210, 211, 211,
   212, 212, 213, 214, 214, 215, 215, 216, 217, 217, 218, 218, 219, 220, 220, 221,
   221, 222, 222, 223, 224, 224, 225, 225, 226, 226, 227, 228, 228, 229, 229, 230,
   230, 231, 231, 232, 233, 233, 234, 234, 235, 235, 236, 236, 237, 237, 238, 238,
   239, 240, 240, 241, 241, 242, 242, 243, 243, 244, 244, 245, 245, 246, 246, 247,
   247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252, 253, 253, 254, 254, 255,
};

// Tabla para Gamma 2
const uint8_t gamma_lut2[256] = {
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,
     1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   4,   4,
     4,   4,   5,   5,   5,   5,   6,   6,   6,   7,   7,   7,   8,   8,   8,   9,
     9,   9,  10,  10,  11,  11,  11,  12,  12,  13,  13,  14,  14,  15,  15,  16,
    16,  17,  17,  18,  18,  19,  19,  20,  20,  21,  21,  22,  23,  23,  24,  24,
    25,  26,  26,  27,  28,  28,  29,  30,  30,  31,  32,  32,  33,  34,  35,  35,
    36,  37,  38,  38,  39,  40,  41,  42,  42,  43,  44,  45,  46,  47,  47,  48,
    49,  50,  51,  52,  53,  54,  55,  56,  56,  57,  58,  59,  60,  61,  62,  63,
    64,  65,  66,  67,  68,  69,  70,  71,  73,  74,  75,  76,  77,  78,  79,  80,
    81,  82,  84,  85,  86,  87,  88,  89,  91,  92,  93,  94,  95,  97,  98,  99,
   100, 102, 103, 104, 105, 107, 108, 109, 111, 112, 113, 115, 116, 117, 119, 120,
   121, 123, 124, 126, 127, 128, 130, 131, 133, 134, 136, 137, 139, 140, 142, 143,
   145, 146, 148, 149, 151, 152, 154, 155, 157, 158, 160, 162, 163, 165, 166, 168,
   170, 171, 173, 175, 176, 178, 180, 181, 183, 185, 186, 188, 190, 192, 193, 195,
   197, 199, 200, 202, 204, 206, 207, 209, 211, 213, 215, 217, 218, 220, 222, 224,
   226, 228, 230, 232, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255,
  };

// Tabla para Gamma 3
const uint8_t gamma_lut3[256] = {
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,
     2,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   3,   4,   4,
     4,   4,   4,   5,   5,   5,   5,   6,   6,   6,   6,   6,   7,   7,   7,   8,
     8,   8,   8,   9,   9,   9,  10,  10,  10,  11,  11,  12,  12,  12,  13,  13,
    14,  14,  14,  15,  15,  16,  16,  17,  17,  18,  18,  19,  19,  20,  20,  21,
    22,  22,  23,  23,  24,  25,  25,  26,  27,  27,  28,  29,  29,  30,  31,  32,
    32,  33,  34,  35,  35,  36,  37,  38,  39,  40,  40,  41,  42,  43,  44,  45,
    46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  60,  61,  62,
    63,  64,  65,  67,  68,  69,  70,  72,  73,  74,  76,  77,  78,  80,  81,  82,
    84,  85,  87,  88,  90,  91,  93,  94,  96,  97,  99, 101, 102, 104, 105, 107,
   109, 111, 112, 114, 116, 118, 119, 121, 123, 125, 127, 129, 131, 132, 134, 136,
   138, 140, 142, 144, 147, 149, 151, 153, 155, 157, 159, 162, 164, 166, 168, 171,
   173, 175, 178, 180, 182, 185, 187, 190, 192, 195, 197, 200, 202, 205, 207, 210,
   213, 215, 218, 221, 223, 226, 229, 232, 235, 237, 240, 243, 246, 249, 252, 255,
  };

// Tabla para Gamma 4
const uint8_t gamma_lut4[256] = {
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
     1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,
     2,   3,   3,   3,   3,   3,   3,   3,   4,   4,   4,   4,   4,   5,   5,   5,
     5,   5,   6,   6,   6,   6,   7,   7,   7,   7,   8,   8,   8,   9,   9,   9,
     9,  10,  10,  11,  11,  11,  12,  12,  13,  13,  13,  14,  14,  15,  15,  16,
    16,  17,  17,  18,  18,  19,  19,  20,  21,  21,  22,  23,  23,  24,  25,  25,
    26,  27,  27,  28,  29,  30,  31,  31,  32,  33,  34,  35,  36,  37,  38,  39,
    40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  52,  53,  54,  55,  57,
    58,  59,  61,  62,  63,  65,  66,  68,  69,  71,  72,  74,  75,  77,  79,  80,
    82,  84,  85,  87,  89,  91,  93,  95,  96,  98, 100, 102, 104, 107, 109, 111,
   113, 115, 117, 120, 122, 124, 126, 129, 131, 134, 136, 139, 141, 144, 146, 149,
   152, 155, 157, 160, 163, 166, 169, 172, 175, 178, 181, 184, 187, 190, 194, 197,
   200, 203, 207, 210, 214, 217, 221, 224, 228, 232, 236, 239, 243, 247, 251, 255,
  };

// Tabla para Gamma 5
const uint8_t gamma_lut5[256] = {
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,
     1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,
     2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   3,   4,   4,   4,
     4,   4,   5,   5,   5,   5,   5,   6,   6,   6,   6,   7,   7,   7,   8,   8,
     8,   8,   9,   9,   9,  10,  10,  11,  11,  11,  12,  12,  13,  13,  14,  14,
    15,  15,  16,  16,  17,  17,  18,  19,  19,  20,  20,  21,  22,  23,  23,  24,
    25,  26,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
    40,  41,  42,  43,  45,  46,  47,  49,  50,  51,  53,  54,  56,  57,  59,  60,
    62,  63,  65,  67,  68,  70,  72,  74,  76,  78,  80,  82,  84,  86,  88,  90,
    92,  94,  97,  99, 101, 104, 106, 109, 111, 114, 116, 119, 122, 125, 128, 130,
   133, 136, 139, 143, 146, 149, 152, 156, 159, 162, 166, 170, 173, 177, 181, 184,
   188, 192, 196, 200, 205, 209, 213, 217, 222, 226, 231, 236, 240, 245, 250, 255,
  };


// Función de correción Gamma.
void GammaCorrection(Mat& src, Mat& dst, float fGamma){
	unsigned char lut[256];

	for (int i = 0; i < 256; i++){
		lut[i] = saturate_cast<uchar>(pow((float)(i / 255.0), fGamma) * 255.0f);
	}

	dst = src.clone();
	const int channels = dst.channels();
	switch (channels){

		case 1:{
			MatIterator_<uchar> it, end;
			for (it = dst.begin<uchar>(), end = dst.end<uchar>(); it != end; it++)
				*it = lut[(*it)];
			break;
		}

		case 3:{
			MatIterator_<Vec3b> it, end;
			for (it = dst.begin<Vec3b>(), end = dst.end<Vec3b>(); it != end; it++){
				(*it)[0] = lut[((*it)[0])];
				(*it)[1] = lut[((*it)[1])];
				(*it)[2] = lut[((*it)[2])];
			}
			break;
		}
	}
}


// Función de correción pixel a pixel.
void corregir_pixel(Mat& img, float gamma_value, int X, int Y, int W, int H, int R, int G, int B){
    cv::Mat M_YUV, M_YUV_Gamma, img_out, img_border;
    vector<cv::Mat> planes;
    cv::cvtColor(img, M_YUV, cv::COLOR_BGR2YCrCb);
    cv::split(M_YUV, planes);
    GammaCorrection(planes[0], planes[0], gamma_value);
    cv::merge(planes, M_YUV_Gamma);
    //cv::imshow("Imagen en YUV con correccion Gamma", M_YUV_Gamma);

    // Se convierte la imágen de espacio de color YUB a BGR.
    cv::cvtColor(M_YUV_Gamma, img_out, cv::COLOR_YCrCb2BGR);

    // Se recorta el rectángulo a mostrar
    cv::Mat whole = img_out; // Imágen original
    cv::Mat part(
    whole,
    cv::Range( Y, Y+H ), // rows
    cv::Range( X, X+W ));// cols
    
    part.copyTo(img(cv::Rect(X, Y, part.cols, part.rows)));

    // Se genera el borde
    Scalar value(R,G,B);
    copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);

    // Se muestra la imágen corregida
    cv::imshow("Imagen con correcion Gamma por funcion en capa de luminancia", img_border);
} 

// Función de corrección por tabla.
void corregir_tabla(Mat& img, float gamma_value, int X, int Y, int W, int H, int R, int G, int B){
    cv::Mat M_YUV, img_out, img_border, img_aux;
    vector<cv::Mat> planes, canales;
    img_aux = img;

    // Se convierte la imágen de espacio de color BGR a YUV.
    cv::cvtColor(img_aux, M_YUV, cv::COLOR_BGR2YCrCb);
    cv::split(M_YUV, planes);
    
    // Se extraen los valores de las imágenes
    uchar *data_old = M_YUV.data;
    uchar *data_new = img_aux.data;
    
    // Se reemplazan los valores de la imágen por los de las tablas Gamma.
    int i, j, cols = img_aux.cols, rows = img_aux.rows;
    for (i = 0; i < rows*3; i++){
        for (j = 0; j < cols*3; j++){
            if (gamma_value == 0.5) data_new[i*cols+j]= int(gamma_lutp5[data_old[i*cols+j]]);
            if (gamma_value == 2) data_new[i*cols+j]= int(gamma_lut2[data_old[i*cols+j]]);
            if (gamma_value == 3) data_new[i*cols+j]= int(gamma_lut3[data_old[i*cols+j]]);
            if (gamma_value == 4) data_new[i*cols+j]= int(gamma_lut4[data_old[i*cols+j]]);
            if (gamma_value == 5) data_new[i*cols+j]= int(gamma_lut5[data_old[i*cols+j]]);
        }
    }

    // Se compone la nueva imágen a partir del canal de luminancia corregido en gamma junto a los canales de croma originales.
    cv::split(img_aux, canales);
    canales = {canales[0],planes[1],planes[2]};
    cv::merge(canales, img_out);

    // Se convierte la imágen de espacio de color YUV a BGR.
    cv::cvtColor(img_out, img_out, cv::COLOR_YCrCb2BGR);
    cv::cvtColor(M_YUV, img, cv::COLOR_YCrCb2BGR);

    // Se recorta el rectángulo a mostrar
    cv::Mat whole = img_out; // Imágen original
    cv::Mat part(
    whole,
    cv::Range( Y, Y+H ), // rows
    cv::Range( X, X+W ));// cols
    
    part.copyTo(img(cv::Rect(X, Y, part.cols, part.rows)));

    // Se genera el borde
    Scalar value(R,G,B);
    copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
    cv::imshow("Imagen con correcion Gamma por tabla en capa de luminancia", img_border);
}

int main(int argc, char *argv[]){

    // Valores booleanos que determinan el tipo de procesamiento a realizar.
	bool tabla = false, pixel = false, imagen = false, video = false;
    int R = 0, G = 0, B = 0;
    int X = 0, Y = 0, W, H;
	
    // Muestra mensaje error en caso de utilizar menos de 4 argumentos o más de 6.
	if(argc < 4) {
        cerr << "Usage: ./GAMMA [-m1 | -m2] -i image gamma [-f x y w h] [-c r g b]" << endl;
        cerr << "Usage: ./GAMMA [-m1 | -m2] -v gamma [-f x y w h] [-c r g b]" << endl;
        return 1;
    }

    // Encuentra el valor "i" en el segundo argumento.
    if ((argv[2][1])==105 || (argv[2][1])==73){
    	imagen = true;
    	cout<<"Procesamiento de imagen ";
    }

    // Encuentra el valor "v" en el segundo argumento.
    if ((argv[2][1])==118 || (argv[2][1])==86){
    	video = true;
    	cout<<"Procesamiento de video ";
    }

    // Encuentra el valor "-m1" en el primer argumento.
    if ((argv[1][2])==49){
    	tabla = true;
		cout<<"por tabla, ";
	}

    // Encuentra el valor "-m2" en el primer argumento.
    if ((argv[1][2])==50){
    	pixel = true;
    	cout<<"pixel a pixel, ";
    }


    cv::Mat img, img_out;
    float gamma_value;

    // Lógica de procesamiento de imágen.
    if (imagen){
        // Lee la imágen
    	img = cv::imread(argv[3], 1);
        R = G = B = X = Y = 0;
        W = img.cols;
        H = img.rows;

        // Si no se encuentra la imágen. 
	    if(img.empty()) {
	        cerr << "Error reading image " << argv[3] << endl;
	        return 1;
	    }

        // Guarda el valor de Gamma
	    gamma_value = atof(argv[4]);
    	cout<<"nivel gamma : "<<gamma_value<<endl;
    	//cv::imshow("Imagen original", img);

        // Generador de bordes
        cv::Mat img_border, img_out_border;
        Scalar value(0,0,0);
        copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);

        if(argc == 9){ // Solo definición de borde
            if ((argv[5][1])==99 || (argv[5][1])==67){ // c ó C
                R = atof(argv[8]);
                G = atof(argv[7]);
                B = atof(argv[6]);
                Scalar value(R,G,B);
                copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
            }
        }

        if(argc == 10){ // Solo definición de rectángulo
            if ((argv[5][1])==102 || (argv[5][1])==70){ // f ó F
                X = atof(argv[6]);
                Y = atof(argv[7]);
                W = atof(argv[8]);
                H = atof(argv[9]);
                //cout<<"X: "<<X<<" Y: "<<Y<<" W: "<<W<<" H: "<<H<<endl;
            }
        }

        if(argc>10){ // Ambas definiciones
            if ((argv[5][1])==102 || (argv[5][1])==70){ // f ó F
                X = atof(argv[6]);
                Y = atof(argv[7]);
                W = atof(argv[8]);
                H = atof(argv[9]);
                cout<<"X: "<<X<<" Y: "<<Y<<" W: "<<W<<" H: "<<H<<endl;
            }
            if ((argv[10][1])==99 || (argv[10][1])==67){ // c ó C
                R = atof(argv[13]);
                G = atof(argv[12]);
                B = atof(argv[11]);
                Scalar value(R,G,B);
                copyMakeBorder(img, img_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
            }   
        }
        
        cv::imshow("Imagen original", img_border);

        cout << "Press any key to terminate" << endl;


        // Corrección Gamma con función.
        //if (pixel) corregir_pixel(img, gamma_value, R, G, B);
        if (pixel) corregir_pixel(img, gamma_value, X, Y, W, H, R, G, B);
            
        // Corrección Gamma con tabla.
        if (tabla) corregir_tabla(img, gamma_value, X, Y, W, H, R, G, B);
    }
        


    // Lógica de procesamiento de video.
    if (video){
        gamma_value = atof(argv[3]);
        cout<<"nivel gamma : "<<gamma_value<<endl;

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
            cerr << "ERROR! Unable to open camera\n";
            return -1;
        }
        
        // Loop de captura.
        cout << "Start grabbing" << endl
        << "Press any key to terminate" << endl;
        for (;;){
            // Esperar por u nuevo frame.
            cap.read(frame);
            R = G = B = X = Y = 0;
            W = frame.cols;//1280;
            H = frame.rows;//720;

            // Revisar si no hay errores.
            if (frame.empty()) {
                cerr << "ERROR! blank frame grabbed\n";
                break;
            }

            cv::Mat frame_border;
            Scalar value(R,G,B);

            copyMakeBorder(frame, frame_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
            if(argc == 8){ // Solo definición de borde
                if ((argv[4][1])==99 || (argv[4][1])==67){ // c ó C
                    R = atof(argv[7]);
                    G = atof(argv[6]);
                    B = atof(argv[5]);
                    Scalar value(R,G,B);
                    copyMakeBorder(frame, frame_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
                }
            }
            if(argc == 9){ // Solo definición de rectángulo
                if ((argv[4][1])==102 || (argv[4][1])==70){ // f ó F
                    X = atof(argv[5]);
                    Y = atof(argv[6]);
                    W = atof(argv[7]);
                    H = atof(argv[8]);
                } 
            }

            else if(argc>9){ // Ambas definiciones
                if ((argv[4][1])==102 || (argv[4][1])==70){ // f ó F
                    X = atof(argv[5]);
                    Y = atof(argv[6]);
                    W = atof(argv[7]);
                    H = atof(argv[8]);
                }   
                if ((argv[9][1])==99 || (argv[9][1])==67){ // c ó C
                    R = atof(argv[12]);
                    G = atof(argv[11]);
                    B = atof(argv[10]);
                    Scalar value(R,G,B);
                    copyMakeBorder(frame, frame_border, borde, borde, borde, borde, BORDER_CONSTANT, value);
                }
            }


            imshow("Video original", frame_border);
            // Corrección Gamma con función.
            if (pixel) corregir_pixel(frame, gamma_value, X, Y, W, H, R, G, B);
            // Corrección Gamma con tabla.
            if (tabla) corregir_tabla(frame, gamma_value, X, Y, W, H, R, G, B);

            
            // *** JUST FOR FUN ***
            /*
            cv::Mat F_HSV, F_HLS, M2, MB, MG;
            vector<cv::Mat> planes, planesb, planesg, planesr, cHSV, cHLS;

            cv::cvtColor(frame, F_HLS, cv::COLOR_BGR2HLS);
            cv::imshow("Video en HLS", F_HLS);
            cv::split(F_HLS, cHLS);
            // HUE
            cv::imshow("HLS - HUE", cHLS[0]);
            // LIGHT
            cv::imshow("HLS - LIGHT", cHLS[1]);
            // SAT
            cv::imshow("HLS - SAT", cHLS[2]);

            cv::cvtColor(frame, F_HSV, cv::COLOR_BGR2HSV);
            cv::imshow("Video en HSV", F_HSV);
            cv::split(F_HSV, cHSV);
            // HUE
            cv::imshow("HSV - HUE", cHSV[0]);
            // SAT
            cv::imshow("HSV - SAT", cHSV[1]);
            // VAL
            cv::imshow("HSV - VAL", cHSV[2]);
            
            M2 = MB = MG = MR = frame;

            cv::split(M2, planes);
            cv::split(MB, planesb);
            cv::split(MG, planesg);
            cv::split(MR, planesr);

            // No Blue
            planesb[0] = 0;
            planesb = {planesb[0],planes[1],planes[2]};
            cv::merge(planesb, MB);
            cv::imshow("No Blue", MB);

            // No Green
            planesg[1] = 0;
            planesg = {planes[0],planesg[1],planes[2]};
            cv::merge(planesg, MG);
            cv::imshow("No Green", MG);

            // No Red
            planesr[2] = 0;
            planesr = {planes[0],planes[1],planesr[2]};
            cv::merge(planesr, MR);
            cv::imshow("No Red", MR);
            */
            // **** JUST FOR FUN ***


            if (waitKey(5) >= 0)
                break;  
        }
        return 0;
    }

    waitKey(0);
    return 0;
}






