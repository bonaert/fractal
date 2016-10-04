#include <iostream>
#include <fstream>
#include <stdlib.h>

const int HEIGHT = 500;
const int WIDTH = 500;
const int DEPTH = 80;


int get_iterations(float c, float d){
	// (a + bi)*(a + b*i) + (c + di)
	// Real: a² - b² + c
	// Real: (2ab + d)i

	float x = 0;
	float y = 0;
	int iterations = 0;

	while (x*x + y*y <= 4 and iterations < DEPTH){
		float old_x = x;
		x = x*x - y*y + c;
		y = 2*old_x*y + d;
		iterations++;
	}

	return iterations;

}

void generate_numbers(int iterations[HEIGHT][WIDTH], float start_x, float start_y, float end_x, float end_y){
	float delta_x = (end_x - start_x) / (WIDTH - 1);
	float delta_y = (end_y - start_y) / (HEIGHT - 1);

	float x = start_x;
	float y = start_y;

	for (int i = 0; i < HEIGHT; ++i){

		for (int j = 0; j < WIDTH; ++j)
		{
			iterations[i][j] = get_iterations(x, y);
			x += delta_x;
		}

		y += delta_y;
		x = start_x;
	}
}

int main(int argc, char** argv){
	if (argc == 5){
		float start_x = atof(argv[1]);
		float start_y = atof(argv[2]);
		float end_x = atof(argv[3]);
		float end_y = atof(argv[4]);


		int numbers[HEIGHT][WIDTH];
		generate_numbers(numbers, start_x, start_y, end_x, end_y);

		std::ofstream myfile;
		myfile.open("iterations.txt");
		for (int i = 0; i < HEIGHT; ++i){
			for (int j = 0; j < WIDTH; ++j)
			{
				myfile << numbers[i][j] << " ";
			}
			myfile << std::endl;
		}
		myfile.close();
	} else {
		std::cout << "Wrong number of parameters" << std::endl << "Please pass 4 floats" << std::endl;
	}
	

	


	return 0;
}