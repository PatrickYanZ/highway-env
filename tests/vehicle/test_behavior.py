import pytest

from highway_env.vehicle.objects import Obstacle
from highway_env.road.road import Road, RoadNetwork
from highway_env.vehicle.behavior import IDMVehicle, LinearVehicle
from highway_env.vehicle.kinematics import Vehicle

FPS = 15
vehicle_types = [IDMVehicle, LinearVehicle]


@pytest.mark.parametrize("vehicle_type", vehicle_types)
def test_stop_before_obstacle(vehicle_type):
    road = Road(RoadNetwork.straight_road_network(lanes=1))
    # vehicle = vehicle_types(road=road, position=[0, 0], speed=20, heading=0)
    vehicle = Vehicle(road=road, position=[0, 0], speed=20, heading=0)
    obstacle = Obstacle(road=road, position=[80, 0])
    road.vehicles.append(vehicle)
    road.objects.append(obstacle)
    for _ in range(10 * FPS):
        road.act()
        road.step(dt=1/FPS)
    print(vehicle.position[0],vehicle.position[1])
    print(obstacle.position[0],obstacle.position[1])
    assert not vehicle.crashed
    assert vehicle.position[0] == pytest.approx(obstacle.position[0] - vehicle_type.DISTANCE_WANTED, abs=1)
    assert vehicle.position[1] == pytest.approx(0)
    assert vehicle.speed == pytest.approx(0, abs=1)
    assert vehicle.heading == pytest.approx(0)

if __name__ == "__main__":
    test_stop_before_obstacle(vehicle_types)