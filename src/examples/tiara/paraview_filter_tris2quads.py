"""
Filter script can be used in ProgrammableFilter after TIARA.

Description of the use of the paraview_filter_tris2quads:

1. In Paraview, open case with a triangular mesh.
2. Open the tree structure for StreamLinesTracer, then select 'Triangulation' and 
'RemoveUnusedPoints'.
3. Right-click on mouse -> Add Filter -> Aplhabetical -> Programmable Filter
4. Copy 
exec(open('/home/campus70/solps-gui/src/examples/tiara/paraview_filter_tris2quads.py').read())
in the 'Script' window and make sure that you tick the 'Copy Arrays' box!
5. Press 'Apply' and when you have made this ProgrammableFilter visible, you 
should see quadrilaterals on your mesh.
"""

import numpy as np
import paraview

input_triangulation = inputs[0]
input_streamlines = inputs[1]

class Tris2Quads():
   """
   This class converts flux aligned triangles into quads that have 2 flux
   aligned edges (X_aligned_edges) and 2 streamlined edges (one of
   Y_aligned_edges that is radial aligned). If these requests for quads are
   not valid, then triangles (or edges) remain.
   """

   def __init__(self) -> None:
      """
      Sets up the initial data structures and attributes for quads.

      Attributes:
         -triangle_ids (set): A set of all triangle IDs.
         -point_neighbours (dict): A dictionary where the keys are point IDs,
          and the values are sets of triangle IDs.
         -triangle_points (dict): A dictionary where the keys are triangle
          IDs, and the values are sets of point IDs.
         -adjacent_triangles (dict): A dictionary where the keys are tuples of
          two points (representing an edge), and the values are sets of
          adjacent triangle.
         -streamlines (list): A list of streamlines, each containing sets of
          point IDs.
         -y_aligned_edges (set): A set of edges represented as tuples of point
          ID pairs (id1, id2) with id1 < id2.
         -levelIds_array: An optional attribute that can be set as needed.
      """
      self.triangle_ids = set()
      self.point_neighbours = dict()
      self.triangle_points = dict()
      self.adjacent_triangles = dict()
      self.streamlines = list()
      self.y_aligned_edges = set() 
      self.levelIds_array = None
      # TODO clear_data before prepare data if called twice

   def prepare_data(self, input_triangulation, input_streamlines, output_mesh):
      """
      This function processes the input triangulation and streamlines to prepare
      internal data structures that will be used for fast edge search.

      Parameters:
      - input_triangulation: The input triangulation data.
      - input_streamlines: The input streamlines data.
      - output_mesh: The VTK mesh where processed data is stored, including
        triangles and lines derived from the input data.
      """
      #self.point_neighbours.clear()
      #self.triangle_ids.clear()
      #self.triangle_points.clear()
      #self.adjacent_triangles.clear()
      self.levelIds_array = input_triangulation.PointData["LevelIds"]
      num_cells = input_triangulation.GetNumberOfCells()
      output_mesh.Allocate(1, num_cells) #clear output for new mesh
      for i in range(num_cells):
         cell = input_triangulation.GetCell(i)
         pts = cell.GetNumberOfPoints()
         id0 = cell.GetPointId(0)
         id1 = cell.GetPointId(1)
         if pts == 3: # Point ids for triangles
            id2 = cell.GetPointId(2)
            self.triangle_ids.add(i)    
            self.insert_triangle_point(i, id0)
            self.insert_triangle_point(i, id1)
            self.insert_triangle_point(i, id2)
            self.insert_triangle(i, id0, id1, id2)
            self.insert_triangle_edges(i)
         elif pts == 2: # Point ids for edges (streamlines)
            ptIds = vtk.vtkIdList()
            ptIds.SetNumberOfIds(2)
            ptIds.SetId(0, id0)
            ptIds.SetId(1, id1)
            output_mesh.InsertNextCell(vtk.VTK_LINE, ptIds)

      #self.streamlines.clear()
      #self.y_aligned_edges.clear()
      num_cells = input_streamlines.GetNumberOfCells()
      for i in range(num_cells):
         cell = input_streamlines.GetCell(i)
         num_pts = cell.GetNumberOfPoints()
         if num_pts > 2:
            streamline = set()
            previous_id = None
            for j in range(num_pts):
               id = cell.GetPointId(j)
               streamline.add(id)
               if previous_id:
                  edge = (previous_id, id) if previous_id < id else (id, previous_id) # y_aligned_edge is: if first point id is always smaller than the second point id
                  self.y_aligned_edges.add(edge)
               previous_id = id
            self.streamlines.append(streamline)

   def insert_triangle_point(self, triangle_id, point_id):
      """
      Inserts points association with triangles.
      """
      if point_id not in self.point_neighbours:
         self.point_neighbours[point_id] = set()
      self.point_neighbours[point_id].add(triangle_id)

   def insert_triangle_edges(self, triangle_id):
      """
      This function is used to obtein information about triangles sharing
      common edges.It iterates through the points of the triangle to identify
      its edges.For each edge, it ensures that it is stored in the internal
      data structure as (pt1, pt2), where pt1 < pt2.
      """
      points = self.triangle_points[triangle_id]
      for i in points:
         edge = points.copy()
         edge.remove(i)
         (pt1, pt2) = tuple(edge) # set is unhashable type

         if pt1 < pt2 and (pt1, pt2) not in self.adjacent_triangles:
            self.adjacent_triangles[(pt1, pt2)] = set()
         elif pt2 < pt1 and (pt2, pt1) not in self.adjacent_triangles:
            self.adjacent_triangles[(pt2, pt1)] = set()
         if pt1 < pt2:
            self.adjacent_triangles[(pt1, pt2)].add(triangle_id)
         else:
            self.adjacent_triangles[(pt2, pt1)].add(triangle_id)

   def insert_triangle(self, triangle_id, id0, id1, id2):
      """
      This function inserts point IDs of a triangle into the data structure.
      """
      self.triangle_points[triangle_id] = set([id0, id1, id2])

   #def get_triangle_neighbours(self, triangle_id):
   #  points = self.triangle_points[triangle_id]
   #  neighbour_triangle_ids = set()
   #  for id in points:
   #     neighbour_triangle_ids.update(self.point_neighbours[id])
   #  neighbour_triangle_ids.remove(triangle_id)
   #  return neighbour_triangle_ids

   def get_adjacent_triangles(self, triangle_id):
      """
      Find neighbouring triangles with common edges.
      """
      my_adjacent_triangles = set()
      points = self.triangle_points[triangle_id]
      for i in points:
         edge = points.copy()
         edge.remove(i)
         pt1, pt2 = tuple(edge)
         edge = (pt1, pt2) if pt1 < pt2 else (pt2, pt1)
         my_adjacent_triangles.update(self.adjacent_triangles[edge])
      my_adjacent_triangles.remove(triangle_id)
      return my_adjacent_triangles

   def try_to_merge_triangle(self, triangle_id, output):
      """
      There must be two flux aligned edges with different
      levelId and two edges on a streamline for two adjacent
      triangles to qualify for a flux aligned quad.

      Parameters:
      - output: The VTK mesh where processed data is stored, including
        quads and points.
      """
      my_adjacent_triangles = self.get_adjacent_triangles(triangle_id)
      points = self.triangle_points[triangle_id]
      x_aligned_edge = None # pt1 levelId == pt2 levelId
      y_aligned_edge = None 
      common_edge = None # Third edge which connects x_aligned_edge and y_aligned_edge
      for i in points: # loop through point-adjacent edges
         edge = points.copy()
         edge.remove(i)
         (pt1, pt2) = tuple(edge)
         edge = (pt1, pt2) if pt1 < pt2 else (pt2, pt1)
         if self.levelIds_array[pt1] ==  self.levelIds_array[pt2]:
            x_aligned_edge = edge
            #print(f"x aligned edge {edge}")
            continue
         if edge in self.y_aligned_edges:
            y_aligned_edge = edge
            #print(f"y_aligned_edge {y_aligned_edge}")
            continue
         common_edge = edge

         adjacent_triangle = self.adjacent_triangles[common_edge]
         # Checking if there's only one adjacent triangle related to the common_edge.
         if len(adjacent_triangle) == 1:
            return False
         adjacent_triangle = adjacent_triangle.copy()
         adjacent_triangle.remove(triangle_id)
         adjacent_triangle = adjacent_triangle.pop()
         #print(f"Adjacent triangle: {adjacent_triangle}")
 
      if x_aligned_edge is not None and y_aligned_edge is not None:
         #print(f"We can merge with triangle {adjacent_triangle} having common edge {common_edge} consisting of points {self.triangle_points[adjacent_triangle]}")
         adjacent_triangle_points = self.triangle_points[adjacent_triangle]
         adjacent_point = adjacent_triangle_points.difference(common_edge).pop()
         #print(f"Adjacent point {adjacent_point}")
         #edge3 = (pt1, adjacent_point) if pt1 < adjacent_point else (adjacent_point, pt1)
         #edge4 = (pt2, adjacent_point) if pt2 < adjacent_point else (adjacent_point, pt2)
         ##print(f"Two edges {edge3} and {edge4}")

         adjacent_x_aligned_point = self.triangle_points[triangle_id].difference(x_aligned_edge).pop()
         adjacent_x_aligned_edge = (adjacent_x_aligned_point, adjacent_point) if adjacent_x_aligned_point < adjacent_point else (adjacent_point, adjacent_x_aligned_point)
         #print(f"adjacent_x_aligned_edge {adjacent_x_aligned_edge}")

         adjacent_y_aligned_point = self.triangle_points[triangle_id].difference(y_aligned_edge).pop()
         adjacent_y_aligned_edge = (adjacent_y_aligned_point, adjacent_point) if adjacent_y_aligned_point < adjacent_point else (adjacent_point, adjacent_y_aligned_point)
         #print(f"adjacent_y_aligned_edge {adjacent_y_aligned_edge}")

         if adjacent_y_aligned_edge in self.y_aligned_edges and self.levelIds_array[adjacent_x_aligned_point] ==  self.levelIds_array[adjacent_point]:
            #print(f"We can truly merge triangles {triangle_id} and {adjacent_triangle}")

            point = self.triangle_points[triangle_id].difference(common_edge).pop()
            ptIds = vtk.vtkIdList()
            ptIds.SetNumberOfIds(4)
            ptIds.SetId(0, adjacent_y_aligned_point)
            ptIds.SetId(1, point)
            ptIds.SetId(2, adjacent_x_aligned_point)
            ptIds.SetId(3, adjacent_point)
            output.InsertNextCell(vtk.VTK_QUAD, ptIds)
            # TODO orientation CW/CCW?(-now is CCW)Critical and Boundary data needed?
            #print(f"Creating Quad: {adjacent_y_aligned_point}, {point}, {adjacent_x_aligned_point}, {adjacent_point}")
            self.triangle_ids.remove(triangle_id)
            self.triangle_ids.remove(adjacent_triangle)
            return True
      return False

   def convertTrianglesToQuads(self, output):
      """
      Main loop with a copy of the triangles that are removed when they become
      quads. If a quad cannot be created, a triangle is created instead.
      """
      for i in self.triangle_ids.copy():
         if i in self.triangle_ids:
            if not self.try_to_merge_triangle(i, output):
               # Add triangle back to mesh
               ptIds = vtk.vtkIdList()
               ptIds.SetNumberOfIds(3)
               for j, id in enumerate(self.triangle_points[i]):
                  ptIds.SetId(j, id)
               output.InsertNextCell(vtk.VTK_TRIANGLE, ptIds)
               # TODO orientation CW or CCW?
try:
   tris2quads
except NameError:
   tris2quads = Tris2Quads()
   
tris2quads.prepare_data(input_triangulation, input_streamlines, output)
tris2quads.convertTrianglesToQuads(output)


#numCells = input_streamlines.GetNumberOfCells()
#paraview.logger.info(f'Number of Cells: {numCells}')



#numQuads = input0.GetNumberOfCells()

#quadArray = np.empty(numQuads, dtype=np.float64)
#for i in range(numQuads):
 #      cell = input0.GetCell(i)
 #      p1 = input0.GetPoint(cell.GetPointId(0))
  #     p2 = input0.GetPoint(cell.GetPointId(1))
   #    p3 = input0.GetPoint(cell.GetPointId(2))
    #   p4 = input0.GetPoint(cell.GetPointId(3))
     #  volumeArray[i] = vtk.vtkTetra.ComputeVolume(p1,p2,p3,p4)

#output.CellData.append(quadArray, "Volume")





# num_triangles = 0
# num_lines = 0
# volumeArray = np.empty(numCells, dtype=np.float64)
# for i in range(numCells):
#     cell = input_streamlines.GetCell(i)
#     pts = cell.GetNumberOfPoints()
#     ##print(f"Cell {i} with {pts} points")
#     if pts == 2:
#        num_lines += 1    
#     elif pts == 3:
#        num_triangles += 1
#        id0 = cell.GetPointId(0)
#        id1 = cell.GetPointId(1)
#        id2 = cell.GetPointId(2)
#     volumeArray[i] = 1.0


# paraview.logger.info(f'Lines: {num_lines} Triangles: {num_triangles}')

       #p4 = input_triangulation.GetPoint(cell.GetPointId(3))
       #volumeArray[i] = vtk.vtkTetra.ComputeVolume(p1,p2,p3,p4)

# output.CellData.append(volumeArray, "Volume")

# ptIds = vtk.vtkIdList()
# ptIds.SetNumberOfIds(4)
# ptIds.SetId(0, 422)
# ptIds.SetId(1, 423)
# ptIds.SetId(2, 406)
# ptIds.SetId(3, 405)
# output.InsertNextCell(vtk.VTK_QUAD, ptIds)
# numCells = output.GetNumberOfCells()
# paraview.logger.info(f'Number of Output Cells: {numCells}')

#cell = input_triangulation.GetCell(31)
#ptIds = vtk.vtkIdList()
#ptIds.SetNumberOfIds(100)
#cellIds = vtk.vtkIdList()
#cellIds.SetNumberOfIds(10)

#paraview.logger.info(f'Neighbours: {neighbours.get_triangle_neighbours(32)}')
#paraview.logger.info(f'Adjacent: {neighbours.get_adjacent_triangles(32)}')
#neighbours.try_to_merge_triangle(32, output)
#neighbours.try_to_merge_triangle(36, output)
#neighbours.try_to_merge_triangle(31, output)
#neighbours.try_to_merge_triangle(34, output)


#num_output_cells = output.GetNumberOfCells()
#paraview.logger.info(f'Number of Output Cells: {num_output_cells}')