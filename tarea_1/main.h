/*
 * @function corregir : Esta función recorta la ventana a procesar, hace las conversiones entre espacios de color, hace el llamado entre los distintos tipos de corrección Gamma según corresponda y mide el tiempo de ejecución, fusiona la imagen procesada con la original, y finalmente la muestra en pantalla.
 * @param : imagen a procesar.
 * @return : none.
 *
 * @function corregir_tabla : Esta función realiza una corrección Gamma a la capa de luminancia en una imágen YUV a través de una tabla precalculada.
 * @param : imagen a procesar, valor de Gamma.
 * @return : none.
 *
 * @function corregir_pixel : Esta función realiza una corrección Gamma a la capa de luminancia en una imágen YUV a través de operaciones pixel a pixel.
 * @param : imagen a procesar, valor de Gamma.
 * @return : none.
 */

#pragma once
#include <stdio.h>
#include <iostream>
#include <math.h> 
#include <time.h>
#include <chrono> 
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
using namespace std;
using namespace cv;
using namespace chrono; 

// Variables globales.
#define borde 50 // Ancho del borde.
#define invertir false // Invierte la imagen horizontalmente.
#define timer true // Muestra el timer.
bool tabla = false, pixel = false, imagen = false, video = false; // Tipo de procesamiento a realizar.
int R = 0, G = 0, B = 0, X = 0, Y = 0, W = 1, H = 1; // Color borde, posición, ancho y alto de ventana.
float gamma_value; // Valor de corrección Gamma.
uint promedio;
uint frames;
cv::Mat img, img_roi, img_border; // Matrices de imágenes.

void corregir_tabla(cv::Mat& img, float gamma_value){ // Función de corrección por tabla.
	unsigned char gamma_table[256]; // Creación de la tabla Gamma.
	for (int i = 0; i < 256; i++) gamma_table[i] = cv::saturate_cast<uchar>(pow((float)(i / 255.0), gamma_value) * 255.0f);
	cv::MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = gamma_table[(*it)];
} 

void corregir_pixel(cv::Mat& img, float gamma_value){ // Función de correción pixel a pixel.
	cv::MatIterator_<uchar> it, end;
	for (it = img.begin<uchar>(), end = img.end<uchar>(); it != end; it++) *it = cv::saturate_cast<uchar>(pow((float)(*it/255.0), gamma_value) * 255.0f);
}

void corregir(cv::Mat& img){
	cv::Rect ROI(X, Y, W, H); // Definición de región de interés.
	img_roi = img(ROI); // Asignación de región de interés.
	cv::cvtColor(img_roi, img_roi, cv::COLOR_BGR2YCrCb); // Se convierte la imagen desde BGR a YUV.
	
	auto start = high_resolution_clock::now(); // Se inicia el timer.
	if (tabla) corregir_tabla(img_roi, gamma_value); // Corrección Gamma con tabla.
    if (pixel) corregir_pixel(img_roi, gamma_value); // Corrección Gamma con función.
	auto stop = high_resolution_clock::now(); // Se detiene el timer.
	auto duration = duration_cast<microseconds>(stop - start); // Se calcula la duración del timer.
	promedio+=duration.count();
	if(timer) cout<<"Tiempo de conversión de imagen: "<<duration.count()<<" microsegundos."<< endl;

	cv::cvtColor(img_roi, img_roi, cv::COLOR_YCrCb2BGR); // Se convierte la imagen desde color YUB a BGR.
	img_roi.copyTo(img(ROI)); // Se fusiona la ventana corregida.
	cv::Scalar value(B,G,R); // Se genera vector de valores BGR.
	copyMakeBorder(img, img_border, borde, borde, borde, borde, cv::BORDER_CONSTANT, value); // Se genera el borde.
	cv::imshow("Imagen con correción Gamma en capa de luminancia.", img_border); // Se muestra la imagen corregida.
}