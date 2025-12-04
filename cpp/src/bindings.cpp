#include "../include/board.h"
#include "../include/types.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // For std::vector support

namespace py = pybind11;
using namespace types;
using namespace board;

PYBIND11_MODULE(topcap_engine, m) {
  m.doc() = "Topcap game engine Python bindings";

  // Bind Coordinates
  py::class_<Coordinates>(m, "Coordinates")
      .def(py::init<int, int>(), "Create coordinates", py::arg("x"),
           py::arg("y"))
      .def_readwrite("x", &Coordinates::x)
      .def_readwrite("y", &Coordinates::y);

  // Bind Move (note: 'from' is Python keyword, so we use 'from_' in Python)
  py::class_<Move>(m, "Move")
      .def(py::init<Coordinates, Coordinates>(), "Create move",
           py::arg("from_"), py::arg("to"))
      .def_readwrite("from_", &Move::from, "From coordinates")
      .def_readwrite("to", &Move::to, "To coordinates");

  // Bind Board
  py::class_<Board>(m, "Board")
      .def(py::init<Bitboard, Bitboard, int, bool>(), "Create board",
           py::arg("white"), py::arg("black"), py::arg("N"),
           py::arg("whiteToPlay"))
      .def_readwrite("N", &Board::N)
      .def_readwrite("whiteToPlay", &Board::whiteToPlay);

  // Bind board functions
  m.def("initial_board", &initialBoard, "Create initial board", py::arg("N"));
  m.def("possible_moves", &possibleMoves, "Get possible moves",
        py::arg("board"));
  m.def("make_move", &makeMove, "Make a move", py::arg("board"),
        py::arg("move"));
  m.def("terminal_state", &terminalState, "Check terminal state",
        py::arg("board"));
  m.def("is_move_legal", &isMoveLegal, "Check if move is legal",
        py::arg("board"), py::arg("move"));
  m.def("board_to_string", &boardToString, "Convert board to string",
        py::arg("board"));
}
