import numpy as np
from pprint import pprint 


def parse_input(filename):
    scans = open(filename).read().split("\n\n")
    for i, scan in enumerate(scans):
        scans[i] = [Vector(*[int(i) for i in line.strip().split(",")]) \
                    for line in scan.split("\n")[1:] if line.strip() != ""]

    return scans


class Vector:
    def __init__(self, x, y=0, z=0):
        if isinstance(x, np.ndarray) and x.shape == (3,):
            self.a = x
        else: 
            self.a = np.array([x, y, z], dtype=np.int64)
    
    def __repr__(self):
        return f"[{self.x:5d}, {self.y:5d}, {self.z:5d}]"

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def x(self):
        return self.a[0]
    @x.setter
    def x(self, value):
        self.a[0] = value
    @property
    def y(self):
        return self.a[1]
    @y.setter
    def y(self, value):
        self.a[1] = value
    @property
    def z(self):
        return self.a[2]
    @z.setter
    def z(self, value):
        self.a[2] = value

    def rotate(self, rotation):
        return Vector(np.matmul(self.a, rotation))
    
    def __eq__(self, other):
        return np.all(self.a == other.a)

    def __add__(self, other):
        return Vector(self.a + other.a)

    def __sub__(self, other):
        return Vector(self.a - other.a)


    def manhattan(self, other):
        return abs(self.x - other.x) + \
               abs(self.y - other.y) + \
               abs(self.z - other.z)


# all rotations for case of z being either +z or -z
base_rotations = np.array([
    [[ 1, 0, 0], [ 0, 1, 0], [ 0, 0, 1]],
    [[ 0, 1, 0], [-1, 0, 0], [ 0, 0, 1]],
    [[-1, 0, 0], [ 0,-1, 0], [ 0, 0, 1]],
    [[ 0,-1, 0], [ 1, 0, 0], [ 0, 0, 1]],

    [[-1, 0, 0], [ 0, 1, 0], [ 0, 0,-1]],
    [[ 0, 1, 0], [ 1, 0, 0], [ 0, 0,-1]],
    [[ 1, 0, 0], [ 0,-1, 0], [ 0, 0,-1]],
    [[ 0,-1, 0], [-1, 0, 0], [ 0, 0,-1]]
])

# swap axes ie. z -> +x/-x, z -> +y/-y
rotations = np.concatenate((base_rotations, 
                            base_rotations[:,:,[1,2,0]],
                            base_rotations[:,:,[2,0,1]]))


def scan_diff_set(scan):
    # For each beacon in the scan, find the distance to all other beacons
    # Put the distances in a set and add to a dict indexed by source beacon
    relativeDistances = dict()
    for beacon in scan:
        relativeDistances[beacon] = set()
        for second in scan:
            if beacon == second: 
                continue
            relativeDistances[beacon].add(beacon - second)
    return relativeDistances


def translate_diff_set(diffSet, translation):
    # Translate a set - once we match it we need to move to basis coords
    # Values are relative to the key so only the key needs to change
    translated = dict()
    for k, v in diffSet.items():
        translated[k + translation] = v
    return translated


def rotate_set(beaconSet):
    # For a set of beacon distances, apply each possible rotation and return
    # a dict of all possible rotated versions.
    #
    # Save in memory or reproduce each time? 
    # It's 24 rotations * (25 * 24 beacon distances) per scan (27)
    # = 388800 ints + overhead. Could save them all but we'll just
    # regenerate for each scan. 
    rotated = dict()

    for i, rotation in enumerate(rotations):
        rotatedDiffs = dict()
        for beacon, relativeDistances in beaconSet.items():
            diffs = set()
            for d in relativeDistances:
                diffs.add(d.rotate(rotation))
            rotatedDiffs[beacon.rotate(rotation)] = diffs
        rotated[i] = rotatedDiffs

    return rotated


def part2(scanners):
    # Find max Manhattan distance
    maxDistance = 0
    maxPair = None
    for i in scanners:
        for j in scanners:
            if i == j:
                continue
            if i.manhattan(j) > maxDistance:
                maxDistance = i.manhattan(j)
                maxPair = (i, j)

    return maxDistance, maxPair


def solve(scans, debug=False):
    # This is the set of distances between linked/known beacons with 
    # beacon positions relative to scanner 0
    bases = [scan_diff_set(scans[0])]
    # Known beacons relative to scanner 0
    knownBeacons = set(scans[0])
    # Known scanners relative to scanner 0
    knownScanners = [Vector(0,0,0)]

    # Unmatched scanners. Pop them off once they're matched and add to bases.
    unmatched = list(range(1, len(scans)))
    print("Unmatched scanners:", unmatched)
    # Counter for current unmatched scanner 
    attemptMatch = 0
    while len(unmatched) > 0:
        breakout = False
        
        # Take next unmatched scan
        scan = scans[unmatched[attemptMatch]]
        print(f"Attempt matching scanner {unmatched[attemptMatch]}")
        # Get its rotations
        rotated = rotate_set(scan_diff_set(scan))

        # For each rotation of the unmatched scanner's beacon set...
        for rotation, rotatedDiffs in rotated.items():
            # For each individual beacon in that set...
            for beacon, diffs in rotatedDiffs.items():
                # For each set of matched scanner beacons...
                for base in bases:
                    # For each individual beacon in that set... 
                    for baseBeacon, baseDiffs in base.items():
                        # If distance from unmatched beacon to 11 other beacons
                        # is the same as distance from known beacon to 11 other beacons 
                        if len(diffs & baseDiffs) == 11:
                            # It's a match
                            print(f"Matched scanner {unmatched[attemptMatch]}!")

                            # This is translation from scanner 0 to new matched scanner
                            basisTranslation = baseBeacon - beacon

                            knownScanners.append(basisTranslation)
                            
                            bases.append(translate_diff_set(rotatedDiffs, basisTranslation))
                            
                            # For relative distances from new matched beacon to each 
                            # of the other 24 beacons detected by new matched scanner, 
                            # convert to scanner 0 coords and store
                            for diff in diffs:
                                knownBeacons.add(beacon - diff + basisTranslation)

                            # Remove new matched scanner from consideration
                            unmatched.pop(attemptMatch)
                            
                            if debug:
                                print(f"Known beacons ({len(knownBeacons)}):")
                                pprint(knownBeacons)

                                print("Matched known beacon:                    ", baseBeacon)
                                print("Coords of beacon relative to new scanner:", beacon)
                                print("Common distances relative to beacon:")
                                for b in (diffs & baseDiffs):
                                    print(b)
                                print("Rotation matrix for match:")
                                print(rotations[rotation])

                                print("Translation from new scanner to old scanner coords:")
                                print(basisTranslation)

                                print("Known scanner locations:")
                                pprint(knownScanners)

                                print("Remaining scanners:", unmatched)

                                print("=================================================================== \n")
                            else: 
                                print("Remaining scanners:", len(unmatched))
                            
                            # Reset to first unmatched scanner
                            attemptMatch = 0
                            breakout=True
 
                            break

                    # disgusting!
                    if breakout:        
                        break
                if breakout:
                    break
            if breakout:
                break
            
        if not breakout:
            # No matches, try next scanner
            attemptMatch += 1


    if debug:
        pprint(sorted(list(knownBeacons), 
               key=lambda r: r.x * 100000000 + r.y * 10000 + r.z))

    print("Known beacons:     ", len(knownBeacons))
    
    maxDistance, maxPair = part2(knownScanners)
    print("Max Manhattan:     ", maxDistance)
    print("Max Manhattan pair:", *maxPair)
    print("")
    return len(knownBeacons), maxDistance


if __name__=="__main__":
    # # Useful to check rotation function but you'll need 
    # # to adjust set intersection from 11 to 5
    # scans = parse_input("small_sample.txt")

    scans = parse_input("sample.txt")
    assert solve(scans, True) == (79, 3621)


    scans = parse_input("input.txt")
    assert solve(scans) == (323, 10685)
    