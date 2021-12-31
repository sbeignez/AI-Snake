from snake_utils import Direction
import enum

# Agents Enum
class Agents(enum.Enum):
    AGENT_SHORTEST_DISTANCE = "Shortest Distance"
    AGENT_A_STAR = "A*"


class AgentAI():

    def __init__ (self, session, agent_type : Agents):
        self.session = session
        self.agent_type = agent_type

        self.paths = None

    def next_move(self):
        return self._get_next_move()


    def _get_next_move(self):
        if self.agent_type == Agents.AGENT_SHORTEST_DISTANCE:
            return self.next_move_SD()
        if self.agent_type == Agents.AGENT_A_STAR:
            return self.next_move_AS()
            
    def next_move_SD(self):
        # apple = self.session.apple
        # snake = self.session.snake
        body = self.session.snake.body
        head = self.session.snake.head()
        moves = []
        # DOWN
        if head[1] > 1 and (head[0], head[1]-1) not in self.session.snake.body:
            moves.append((head[0], head[1]-1))
        # UP
        if head[1] < self.session.board.rows and (head[0], head[1]+1) not in self.session.snake.body:
            moves.append((head[0], head[1]+1))
        # RIGHT
        if head[0] < self.session.board.cols and (head[0]+1, head[1]) not in self.session.snake.body:
            moves.append((head[0]+1, head[1]))
        # LEFT
        if head[0] > 1 and (head[0]-1, head[1]) not in self.session.snake.body:
            moves.append((head[0]-1, head[1]))

        print("BODY:", self.session.snake.body, "APPLE:", self.session.apple)
        moves.sort( key = lambda x : abs(x[0] - self.session.apple.x) + abs(x[1] - self.session.apple.y), reverse = False)
        print("MOVES:", moves)

        # move = min(moves, key = lambda x : abs(x[0] - apple[0]) + abs(x[1] - apple[1]))

        self.paths = [[move] for move in moves]
        if self.paths:
            direction = Direction( ( self.paths[0][0][0] - self.session.snake.head()[0], self.paths[0][0][1] - self.session.snake.head()[1]))
        else:
            direction = Direction.STOP

        return direction


    def next_move_AS(self):

        def reconstruct_path(came_from, current):
            path = []
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            return path

        block_start = self.session.snake.head()
        block_end = self.session.apple.cell()
        blocks_open = ( { (x,y) for x in range(1, self.session.board.cols +1) for y in range(1, self.session.board.rows+1) } - set(self.session.snake.body) ) | { block_start } # | union

        # print("A* ===============")
        # print("BLOCKS", blocks_open, len(blocks_open))
        # print("START", block_start, "END", block_end, "SNAKE", set(board["snake"]["body"]))

        openSet = {block_start}
        cameFrom = {}

        def distance_L1(block_start, block_end):
            return abs(block_start[0] - block_end[0]) + abs(block_start[0] - block_end[0])


        gScore = { (block[0],block[1]) : None for block in blocks_open }
        gScore[block_start] = 0

        fScore = { (block[0],block[1]) : None for block in blocks_open }
        fScore[block_start] = distance_L1(block_start, block_end)

        while openSet:

            if openSet:
                current = min(openSet, key = lambda x : fScore[x] ) # openSet.get

            if current == block_end:
                path = reconstruct_path(cameFrom, current) + [block_end]
                # print("A* PATH:", path)
                direction = Direction.STOP
                if len(path) >= 2:
                    direction = Direction.dir(path[0], path[1])

                print("AGENT (AI) action:", direction)
                self.paths = [path]
                return direction

            openSet.remove(current)

            neighbors = { (current[0] + direction.value[0], current[1] + direction.value[1]) for direction in Direction.all_dirs() } & blocks_open # &: intersection

            for neighbor in neighbors:
                tentative_gScore = gScore[current] + 1 # d(current, neighbor)
                if gScore[neighbor] == None or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + distance_L1(neighbor, block_end)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        
        return Direction.STOP





if __name__ == '__main__':
    from snake import start_game
    start_game()