#include <chrono>
#include <iostream>
#include <torch/torch.h>

// Code in this section should not be modified
int classifyImage(const torch::Tensor &image) {
  // This function simulates a ML model that takes ~200 ms to run
  // and returns a classification result (detected object class) as an integer.

  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  return torch::randint(0, 1000, {1}).item<int>();
}
// ------------------------------

int main(int argc, char *argv[]) {

  std::cout << "Not Implemented" << std::endl;

  return 0;
}
