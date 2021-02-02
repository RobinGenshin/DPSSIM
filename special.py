
class Special:

    def klee_burst(self,unit_obj,sim):
        for dot in sim.dot_actions:
            if dot.type == "burst" and dot.unit.name == "Klee":
                if sim.chosen_unit.name != "Klee":
                    sim.dot_actions.remove(dot)
                    
