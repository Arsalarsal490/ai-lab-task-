# Lab 2, Task 3: Stateful Classroom Agent
# ECO, COOL, WARM, and IDLE are simulated modes only.
# No real classroom hardware is controlled.

class ClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):
        # Keep occupancy priority from the original policy.
        if not occupied:
            target_mode = "ECO"
        elif temp > 26:
            target_mode = "COOL"
        elif temp < 20:
            target_mode = "WARM"
        else:
            target_mode = "IDLE"

        # Send a command only when the target mode changes.
        previous_mode = self.previous_mode
        send_command = target_mode != previous_mode

        # Store the new target for the next percept.
        self.previous_mode = target_mode
        return previous_mode, target_mode, send_command


agent = ClassroomAgent()

# Includes a repeated percept, both exact temperature boundaries,
# mode transitions, and an empty-room case.
percepts = [
    (29, True),
    (29, True),
    (20, True),   # exact lower boundary -> IDLE
    (26, True),   # exact upper boundary -> IDLE
    (19, True),   # transition to WARM
    (29, False),  # empty room has priority -> ECO
]

print("Step | Previous mode | Percept (temp, occupied) | Target mode | Outcome")
print("-" * 78)

for step, percept in enumerate(percepts, 1):
    previous, target, send = agent.act(*percept)
    outcome = "COMMAND SENT" if send else "NO COMMAND"
    previous_text = previous if previous is not None else "None"
    print(f"{step:>4} | {previous_text:<13} | {str(percept):<24} | {target:<11} | {outcome}")
