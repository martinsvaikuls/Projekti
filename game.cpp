// Papildd.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <time.h>
#include <SFML/Graphics.hpp>
#include <windows.h>

using namespace std;


class Entity {
private:
	int x;
	int y;
	int health;
	int defense;
	int points;
	int weapon;
	int speed;
	
public:
	
	Entity() : x(0), y(0), health(0), defense(0), points(0), weapon(0), speed(0) {

	}
	Entity(int aX, int aY, int aHealth, int aPoints) : defense(0), weapon(0), speed(0) { // Bonus
		x = aX;
		y = aY;
		health = aHealth;
		points = aPoints;
		
	}
	Entity(int aX, int aY) : health(0), defense(0), points(0), weapon(0), speed(0) { // Enemy
		x = aX;
		y = aY;
	}
	Entity(int aX, int aY, int aHealth, int aDefense, int aWeapon, int aSpeed) : points(0) { // Enemy
		x = aX;
		y = aY;
		health = aHealth;
		defense = aDefense;
		weapon = aWeapon;
		speed = aSpeed;
		
	}

	Entity(int aX, int aY, int aHealth, int aDefense, int aPoints, int aWeapon, int aSpeed) { // Player
		x = aX;
		y = aY;
		health = aHealth;
		defense = aDefense;
		points = aPoints;
		weapon = aWeapon;
		speed = aSpeed;
		
	}

	void setX(int aX) { this->x = aX; }
	void setY(int aY) { this->y = aY; }
	void setHealth(int aHealth) { this->health = aHealth; }
	void setDefense(int aDefense) { this->defense = aDefense; }
	void setPoints(int aPoints) { this->points = aPoints; }
	void setWeapon(int aWeapon) { this->weapon = aWeapon; }
	void setSpeed(int aSpeed) { this->speed = aSpeed; }
	

	int getX() { return x; }
	int getY() { return y; }
	int getHealth() { return health; }
	int getDefense() { return defense; }
	int getPoints() { return points; }
	int getWeapon() { return weapon; }
	int getSpeed() { return speed; }
	

};

class Player : public Entity {
private:

public:
	Player() : Entity() {}
	Player(int aX, int aY, int aHealth, int aDefense, int aPoints, int aWeapon, int aSpeed) : Entity(aX, aY, aHealth, aDefense, aPoints,  aWeapon, aSpeed) {
		
	}
	void weaponUpgrade() { setWeapon(getWeapon() + 1); }
};

class Enemy : public Entity {
private:
	int winPoints;
public:
	Enemy() : Entity() {}
	Enemy(int aX, int aY) : Entity(aX, aY) {
		classGiver();
	}
	
	void setWinPoints(int health, int defense, int weapon, int speed) { winPoints = health/(max(1,2-defense)) * weapon*speed; }

	int getWinPoints() { return winPoints; }

	void classGiver() {
		int healthBonus = rand() % 6;
		int defenseBonus = rand() % 5;
		int weaponBonus = rand() % 3;
		int speedBonus = rand() % 2;
		vector<int> classStats;
		switch (rand() % 3) {
			case 0: // fast
				classStats = { 8,3,2,4 }; //if player damage 2 entityAttack = (max(1,attack-defense) //8  // 16
				break;
			case 1: // tank
				classStats = { 20,8,1,1 }; //20 // 20
				break;
			case 2: // highDamage
				classStats = { 4,0,10,1 }; //2 // 20
				break;
		}
		setHealth(classStats[0] + healthBonus);
		setDefense(classStats[1] + defenseBonus);
		setWeapon(classStats[2] + weaponBonus);
		setSpeed(classStats[3] + speedBonus);
		setWinPoints(getHealth(), getDefense(), getWeapon(), getSpeed());
	}

};

class Bonus : public Entity {
private:
	int giveHealth;
public:
	Bonus() : giveHealth(0), Entity() {}
	Bonus(int aX, int aY, int aHealth, int aPoints) : Entity(aX, aY, aHealth, aPoints) {
		giveHealth = aHealth;
	}
	int getHealth() { return giveHealth; }
};

class Node {
private:
	Node* up;
	Node* right;
	Node* down;
	Node* left;
	Enemy* enemy;
	Player* player;
	Bonus* bonus;
	bool visited;

public:
	Node() : up(nullptr), right(nullptr), down(nullptr), left(nullptr), enemy(nullptr), player(nullptr), bonus(nullptr), visited(false) {
	}
	Node(bool visited) : up(nullptr), right(nullptr), down(nullptr), left(nullptr), enemy(nullptr), player(nullptr), bonus(nullptr) {
		this->visited = visited;
	}
	//~Node();

	void setUp(Node& node) { this->up = &node; }
	void setRight(Node& node) { this->right = &node; }
	void setDown(Node& node) { this->down = &node; }
	void setLeft(Node& node) { this->left = &node; }

	Node* getUp() const { return up; }
	Node* getRight() const { return right; }
	Node* getDown() const { return down; }
	Node* getLeft() const { return left; }

	void setEnemy(Enemy* entity) { enemy = entity; }
	void setPlayer(Player* entity) { player = entity; }
	void setVisited(bool pVisited) { visited = pVisited; }
	void setBonus(Bonus* entity) { bonus = entity; }

	Enemy* getEnemy() const { return enemy; }
	Player* getPlayer() const { return player; }
	bool getVisited() const { return visited; }
	Bonus* getBonus() const { return bonus; }



};


enum class StringCommand {
	S,
	M,
	L,
	XL,
	E,
	H,
	F,
	A
};





vector<int> printStartingOptions();
StringCommand hashString(const string&);

void makeMaze(vector<vector<Node>> &, int, int);
bool connectNodes(vector<vector<Node>>&, int, int, int, int);
bool outOfBounds(int, int, int);

void addEnemiesToMap(int, int, vector<Entity*> &);

void gameLoop(vector<vector<Node>> &, Player &, vector<Entity*> &, bool &);

void updateMap(vector<vector<int>> , sf::VertexArray& , int );
void vertexMap(vector<vector<int>>& , vector<vector<Node>>&);

void playerMove(int, vector<vector<Node>>&, Player &);
void playerAttack(vector<vector<int>>& , vector<vector<Node>>& , Player& );
void moveAttack(int, vector<vector<Node>>&, Player&, int &);

void movementDirection(int &, int &, int , vector<vector<Node>>&, bool);

int main()
{	
	
	Player* p = new Player(0, 0, 100, 2, 0, 2, 1);
	srand((unsigned)time(NULL));
	vector<int> gameSettings;
	gameSettings = printStartingOptions();

	//gameSettings.push_back(10);
	//gameSettings.push_back(5);
	//gameSettings.push_back(5);


	int mSize = gameSettings[0];
	bool playerAlive = true;
	int enemyCount = gameSettings[2];

	while (playerAlive) {
		vector<vector<Node>> labyrinth(mSize, vector<Node>(mSize));
		p->setX(0);
		p->setY(0);
		int a = rand() % mSize;
		int b = rand() % mSize;
		makeMaze(labyrinth, a, b);
	
		vector<Entity*> ent;
		addEnemiesToMap(enemyCount, mSize, ent);

		Bonus* bon = new Bonus(1, 1, 1, 2);

		labyrinth[0][0].setPlayer(p);
		for (int i = 0; i < enemyCount; i++) {
			int xi = ent[i]->getX();
			int xj = ent[i]->getY();
			labyrinth[xi][xj].setEnemy(static_cast<Enemy*>(ent[i]));
		}
		labyrinth[1][1].setBonus(bon);

		
		
		
		try {
			gameLoop(labyrinth, *p, ent, playerAlive);
		}
		catch (...) {
			cout << endl;
			cout << "error in gameLoop" << endl;
		}

		//for (int i = 0; i < ent.size(); i++) {
		//	delete ent[i];
		//}
		delete bon;

	}

}

vector<int> printStartingOptions() {
	vector<int> gameSettings;
	string choice = "";
	
	cout << "Choose labyrinth size: " << endl;
	cout << "S:Small: 5, M:Medium: 10, L:Large: 15, XL:ExtraLarge: 25" << endl;
	while (choice != "S" && choice != "M" && choice != "L" && choice != "XL") {
		cin >> choice;
		for (int i = 0; i < choice.length(); i++) {
			choice[i] = toupper(choice[i]);
		}
	}
	switch (hashString(choice)) {
		case StringCommand::S:
			gameSettings.push_back(5);
			break;
		case StringCommand::M:
			gameSettings.push_back(10);
			break;
		case StringCommand::L:
			gameSettings.push_back(15);
			break;
		case StringCommand::XL:
			gameSettings.push_back(25);
			break;
	}

	

	// S, M, L, XL
	choice = "";
	cout << "Choose difficulty: " << endl;
	cout << "E:Easy, M:Medium, H:Hard" << endl;
	while (choice != "E" && choice != "M" && choice != "H") {
		cin >> choice;
		for (int i = 0; i < choice.length(); i++) {
			choice[i] = toupper(choice[i]);
		}
	}
	switch (hashString(choice)) {
	case StringCommand::E:
		gameSettings.push_back(1);
		break;
	case StringCommand::M:
		gameSettings.push_back(2);
		break;
	case StringCommand::H:
		gameSettings.push_back(4);
		break;
	}
	// E M H
	choice = "";
	cout << "Choose enemy amount: " << endl;
	cout << "F:Few, A:Alot, M:Max" << endl;
	while (choice != "F" && choice != "A" && choice != "M") {
		cin >> choice;
		for (int i = 0; i < choice.length(); i++) {
			choice[i] = toupper(choice[i]);
		}
	}
	int mapCellCount = (gameSettings[0]*gameSettings[0]) - 2;
	switch (hashString(choice)) {
	case StringCommand::F:
		gameSettings.push_back(mapCellCount*20/100);
		break;
	case StringCommand::A:
		gameSettings.push_back(mapCellCount*50/100);
		break;
	case StringCommand::M:
		gameSettings.push_back(mapCellCount);
		break;
	}
	// F A M
	return gameSettings;
}

StringCommand hashString(const string& str) {
	if (str == "S") return StringCommand::S;
	if (str == "M") return StringCommand::M;
	if (str == "L") return StringCommand::L;
	if (str == "XL") return StringCommand::XL;
	if (str == "E") return StringCommand::E;
	if (str == "H") return StringCommand::H;
	if (str == "F") return StringCommand::F;
	if (str == "A") return StringCommand::A;
}


void makeMaze(vector<vector<Node>> &maze, int a, int b) {

	//printTruth(maze);
	int randomNum = rand() % 4;
	int visitedNeighbours = 0;
	int mazeSize = maze.size();
	int a1 = 0;
	int b1 = 0;
	bool toConnect = false;
	cout << randomNum << " ";
	while (true) {
		switch (randomNum) { // up -1 +0 right +0 +1 down +1 +0 left +0 -1 
			case 0: //up down
				a1 = a - 1;
				b1 = b + 0;
				
				toConnect = connectNodes(maze, a, b, a1, b1);
				if (toConnect) {
					maze[a][b].setUp(maze[a1][b1]);
					maze[a1][b1].setDown(maze[a][b]);
					//cout << 'W' << randomNum<< endl;
					makeMaze(maze, a1, b1);
					
				}
				else {
					//cout << 'L';
				}
				
				break;
			case 1: // right left
				a1 = a + 0;
				b1 = b + 1;
				toConnect = connectNodes(maze, a, b, a1, b1);
				if (toConnect) {
					maze[a][b].setRight(maze[a1][b1]);
					maze[a1][b1].setLeft(maze[a][b]);
					//cout << 'W' << randomNum << endl;
					makeMaze(maze, a1, b1);

				}
				else {
					//cout << 'L';
				}
				break;
			case 2: // down up
				a1 = a + 1;
				b1 = b + 0;
				toConnect = connectNodes(maze, a, b, a1, b1);
				if (toConnect) {
					maze[a][b].setDown(maze[a1][b1]);
					maze[a1][b1].setUp(maze[a][b]);
					//cout << 'W' << randomNum << endl;
					makeMaze(maze, a1, b1);

				}
				else {
					//cout << 'L';
				}
				break;
			case 3: // left right
				a1 = a + 0;
				b1 = b - 1;
				toConnect = connectNodes(maze, a, b, a1, b1);
				if (toConnect) {
					maze[a][b].setLeft(maze[a1][b1]);
					maze[a1][b1].setRight(maze[a][b]);
					//cout << 'W' << randomNum << endl;
					makeMaze(maze, a1, b1);

				}
				else {
					//cout << 'L';
				}
				break;
			default:
					cout << "makeMaze switch case thrown out defaultCase" << a << b << randomNum << endl;
				break;
		}

		if (visitedNeighbours > 3)
			break;
		visitedNeighbours++;

		randomNum++;
		randomNum = randomNum % 4;

	}
	
}

bool connectNodes(vector<vector<Node>>& maze, int a, int b, int a1, int b1) {
	int mazeSize = maze.size();
	if (outOfBounds(mazeSize, a1, b1))
		return false;
	if (maze[a1][b1].getVisited() == true)
		return false;
	maze[a][b].setVisited(true); //= Node(true); 
	maze[a1][b1].setVisited(true);// = Node(true); //
	return true;
}

bool outOfBounds(int size, int a, int b) {
	if (a < 0 || b < 0)
		return true;
	if (a >= size || b >= size)
		return true;

	return false;
}

void gameLoop(vector<vector<Node>>& maze, Player &p, vector<Entity*> &ent, bool &playerAlive) {

	cout << "player Pos: " << p.getX() << endl;
	
	float blockSize = 15.f;
	int mazeSize = maze.size();
	unsigned int winSize = (mazeSize * 2 + 1) * 15;


	vector<vector<int>> mazeMapInt(mazeSize*2+1, vector<int>(mazeSize*2+1));

	
	sf::VertexArray mazeMap(sf::PrimitiveType::Triangles);
	mazeMap.resize((mazeSize*2+1) * (mazeSize * 2 + 1) * 6);

	sf::Font font("arial.ttf");
	float textsLocationVertical = 1.f * winSize + 10;
	float textsLocationHorizontal = 25.f;
	int fontSize = 18;
	string strPlHlth = "Player Health: ";
	string strPlPts = "Player Points: ";
	string strEnHlth = "Enemy Health: ";

	sf::Text playerHealth(font);
	playerHealth.setString(strPlHlth);
	playerHealth.setCharacterSize(fontSize);
	playerHealth.setPosition({ textsLocationVertical, textsLocationHorizontal});

	sf::Text playerPoints(font);
	playerPoints.setString(strPlPts);
	playerPoints.setCharacterSize(fontSize);
	playerPoints.setPosition({ textsLocationVertical, textsLocationHorizontal*2});

	sf::Text enemyHealth(font);
	enemyHealth.setString(strEnHlth);
	enemyHealth.setCharacterSize(fontSize);
	enemyHealth.setPosition({ textsLocationVertical, textsLocationHorizontal*3});

	
	sf::RenderWindow window(sf::VideoMode({ winSize * 2, winSize }), "Maze");
	// 1 is wall
	// 0 is path
	// 2 is player
	// 3 is enemy
	// 4 is bonus
	cout << maze.size() << " maze size" << endl;
	cout << mazeMapInt.size() << endl;
	cout << mazeSize * 2 + 1 << endl;
	
	vertexMap(mazeMapInt, maze);
	updateMap(mazeMapInt, mazeMap, mazeSize);
	
	cout << 1 << endl;
	/*
	
	*/

	
	bool isPlayerAttack = false;
	bool playerAction = true;
	bool endGame = false;
	bool isEnemyNear = false;
	int enemyHealthInt = 0;
	mazeMap.resize((mazeSize * 2 + 1) * (mazeSize * 2 + 1) * 6);
	while (window.isOpen())
	{
		if (playerAction)
			while (const std::optional event = window.pollEvent())
			{

				if (event->is<sf::Event::Closed>()) {
					window.close();
					playerAlive = false;
				}

				else if (const auto* keyPressed = event->getIf<sf::Event::KeyPressed>())
				{
					const auto code = keyPressed->scancode;
					if (code == sf::Keyboard::Scancode::Escape) {
						window.close();
						playerAlive = false;
					}
						
					if (playerAction)
						if (isPlayerAttack) {
							// player attack checks if there is an enemy
							
							if (code == sf::Keyboard::Scancode::Up || code == sf::Keyboard::Scancode::W)
								moveAttack(1, maze, p, enemyHealthInt);
							else if (code == sf::Keyboard::Scancode::Right || code == sf::Keyboard::Scancode::D)
								moveAttack(2, maze, p, enemyHealthInt);
							else if (code == sf::Keyboard::Scancode::Down || code == sf::Keyboard::Scancode::S)
								moveAttack(3, maze, p, enemyHealthInt);
							else if (code == sf::Keyboard::Scancode::Left || code == sf::Keyboard::Scancode::A)
								moveAttack(4, maze, p, enemyHealthInt);
							vertexMap(mazeMapInt, maze);
							enemyHealth.setString(strEnHlth + to_string(enemyHealthInt));
							isEnemyNear = true;
							isPlayerAttack = false;
							playerAction = false;
						}
						else {
							if (code == sf::Keyboard::Scancode::Up || code == sf::Keyboard::Scancode::W)
								playerMove(1, maze, p);
							else if (code == sf::Keyboard::Scancode::Right || code == sf::Keyboard::Scancode::D)
								playerMove(2, maze, p);
							else if (code == sf::Keyboard::Scancode::Down || code == sf::Keyboard::Scancode::S)
								playerMove(3, maze, p);
							else if (code == sf::Keyboard::Scancode::Left || code == sf::Keyboard::Scancode::A)
								playerMove(4, maze, p);
							vertexMap(mazeMapInt, maze);
							playerAction = false;

							if (code == sf::Keyboard::Scancode::G) {
								playerAttack(mazeMapInt, maze, p);
								isPlayerAttack = true;
								playerAction = true;
							}
							
							if (code == sf::Keyboard::Scancode::E) {
								if (p.getX() == mazeSize - 1 && p.getY() == mazeSize - 1) {
									window.close();
									playerAlive = true;
									return;
								}
									
							}
							
							
						}

					updateMap(mazeMapInt, mazeMap, mazeSize);
				}
			}
		else // Enemie move???
			for (int i = 0; i < ent.size(); i++) {
				for (int j = 0; j < ent[i]->getSpeed(); j++) {
					//Sleep(100);
					bool forProperWalk = true;
					int vi = 0;
					int pXm = ent[i]->getX();
					int pYm = ent[i]->getY();
					if (maze[pXm][pYm].getEnemy() == nullptr) {
						delete ent[i];
						break;
					}
					int pX = ent[i]->getX();
					int pY = ent[i]->getY();
					int moveDirection = rand() % 4;

					while (forProperWalk) {
						moveDirection = moveDirection + vi % 4;
						movementDirection(pXm, pYm, moveDirection, maze, false);

						if (maze[pXm][pYm].getPlayer() != nullptr) {
							int pHealth = p.getHealth();
							p.setHealth(pHealth - ent[i]->getWeapon());

							playerHealth.setString(strPlHlth + to_string(p.getHealth()));
							enemyHealthInt = ent[i]->getHealth();
							enemyHealth.setString(strEnHlth + to_string(enemyHealthInt));
							cout << "___player health: " << p.getHealth() << endl;
							isEnemyNear = true;
							forProperWalk = false;
							
						}
						else if (maze[pXm][pYm].getEnemy() != nullptr) {
							if (vi > 2)
								forProperWalk = false;
							else
								vi++;
						}
							
						else {
							maze[pXm][pYm].setEnemy(maze[pX][pY].getEnemy());
							maze[pXm][pYm].getEnemy()->setX(pXm);
							maze[pXm][pYm].getEnemy()->setY(pYm);
							maze[pX][pY].setEnemy(nullptr);
							forProperWalk = false;
							

						}
						
					}
					
				}
				vertexMap(mazeMapInt, maze);
				updateMap(mazeMapInt, mazeMap, mazeSize);
				window.clear();
				window.draw(mazeMap);
				window.draw(playerPoints);
				window.draw(playerHealth);
				window.draw(enemyHealth);
				
				window.display();
				
				if (p.getHealth() < 1) {
					// points
					
					endGame = true;
					break;
				}
				
				playerAction = true;
			}
			
			
			
		int plyrPoints = p.getPoints();
		playerPoints.setString(strPlPts + to_string(plyrPoints));
		playerHealth.setString(strPlHlth + to_string(p.getHealth()));
		if (!endGame) {
			window.clear();
			window.draw(mazeMap);
			window.draw(playerPoints);
			window.draw(playerHealth);
			window.draw(enemyHealth);
			window.display();

		}	
		else {
			window.clear();
			window.draw(mazeMap);
			window.draw(playerPoints);
			window.display();
			while (window.isOpen()) {
				while (const std::optional event = window.pollEvent()) {
					if (event->is<sf::Event::Closed>())
					{
						window.close();
						playerAlive = false;
					}
					
					else if (const auto* keyPressed = event->getIf<sf::Event::KeyPressed>()) {
						const auto code = keyPressed->scancode;
						if (code == sf::Keyboard::Scancode::Escape) {
							window.close();
							playerAlive = false;
						}
							
					}
				}
			}
			//cout << "points: " << p.getPoints() << endl;
			//window.close();
		}
		//while (const std::optional event = window.pollEvent() && isPlayerAttack || isPlayerAttack) {
		//
		//}
	}


}

void updateMap(vector<vector<int>> mazeMapInt, sf::VertexArray &mazeMap, int mazeSize) {
	float blockSize = 15.0f;
	for (unsigned int i = 0; i < mazeSize * 2 + 1; ++i) {
		//cout << endl;
		for (unsigned int j = 0; j < mazeSize * 2 + 1; ++j) {
			// get a pointer to the triangles' vertices of the current tile
			sf::Vertex* triangles = &mazeMap[(i + j * (mazeSize * 2 + 1)) * 6];

			// define the 6 corners of the two triangles
			triangles[0].position = sf::Vector2f(i * blockSize, j * blockSize);
			triangles[1].position = sf::Vector2f((i + 1) * blockSize, j * blockSize);
			triangles[2].position = sf::Vector2f(i * blockSize, (j + 1) * blockSize);

			triangles[3].position = sf::Vector2f(i * blockSize, (j + 1) * blockSize);
			triangles[4].position = sf::Vector2f((i + 1) * blockSize, j * blockSize);
			triangles[5].position = sf::Vector2f((i + 1) * blockSize, (j + 1) * blockSize);

			vector<sf::Color> colours{ sf::Color::Black, sf::Color::White, sf::Color::Yellow, sf::Color::Red, sf::Color::Green, sf::Color::Magenta, sf::Color::Cyan};
			sf::Color tileColour = colours[mazeMapInt[j][i]];

			for (int vi = 0; vi < 6; vi++) 
				triangles[vi].color = tileColour;

		}
	}
}

void vertexMap(vector<vector<int>>& mazeMapInt, vector<vector<Node>>& maze) {

	int vertexSize = mazeMapInt.size();
	for (int j = 0; j < vertexSize; j++)
		mazeMapInt[0][j] = 4;

	int vi = 0;
	int vj = 0;

	for (int i = 1; i < vertexSize; i++) {
		mazeMapInt[i][0] = 3;
		//cout << i << 'i ' << endl;
		//cout << vi << 'vi ' << endl;
		vj = 0;
		for (int j = 1; j < vertexSize; j++) {

			if (maze[vi][vj].getEnemy() != nullptr)
				mazeMapInt[i][j] = 3;

			else if (maze[vi][vj].getPlayer() != nullptr)
				mazeMapInt[i][j] = 2;

			else if (maze[vi][vj].getBonus() != nullptr)
				mazeMapInt[i][j] = 4;

			else
				mazeMapInt[i][j] = 0;
			j++;

			//cout << j << ' ';
			if (maze[vi][vj].getRight() != nullptr)
				mazeMapInt[i][j] = 0;
			else
				mazeMapInt[i][j] = 1;
			vj++;

		}
		//cout << endl;
		i++;
		mazeMapInt[i][0] = 1; //
		vj = 0;

		for (int j = 1; j < vertexSize; j++) {

			if (maze[vi][vj].getDown() != nullptr)
				mazeMapInt[i][j] = 0;
			else
				mazeMapInt[i][j] = 1;
			j++;
			mazeMapInt[i][j] = 1;
			vj++;

		}

		vi++;
		//cout << endl;
	}
	
	mazeMapInt[vertexSize - 2][vertexSize - 2] = 5;
}

void playerMove(int moveDirection, vector<vector<Node>>& maze, Player &p) {
	int pX = p.getX();
	int pY = p.getY();
	int pXm = p.getX();
	int pYm = p.getY();
	int pHealth = p.getHealth();
	int pPoints = p.getPoints();
	int bPoints;
	int bHealth;
	//int eWeapon;
	movementDirection(pXm, pYm, moveDirection, maze, true);
	cout << pXm << " " << pX << " " << pYm << " " << pY << endl;
	if (pXm != pX || pYm != pY) {
		cout << "worked " << endl;
		if (maze[pXm][pYm].getEnemy() != nullptr) {
			return;
		}
		//else if (pXm == maze.size() - 1 && pYm == maze.size() - 1)
		//	cout << "";
		else if (maze[pXm][pYm].getBonus() != nullptr) {
			cout << "player health: " << p.getHealth() << endl;
			bPoints = maze[pXm][pYm].getBonus()->getPoints();
			bHealth = maze[pXm][pYm].getBonus()->getHealth();
			p.setPoints(pPoints + bPoints);
			p.setHealth(pHealth + bHealth);
			cout << "player health: " << p.getHealth() << endl;
			maze[pXm][pYm].setBonus(nullptr);
		}

		maze[pX][pY].setPlayer(nullptr);
		maze[pXm][pYm].setPlayer(&p);
		p.setX(pXm);
		p.setY(pYm);
	}
}

void playerAttack(vector<vector<int>>& mazeMapInt,vector<vector<Node>>& maze, Player& p) {
	int pX = p.getX();
	int pY = p.getY();
	//cout << "self: " << &maze[pX][pY] << "   ";
	if (maze[pX][pY].getUp() != nullptr)
		mazeMapInt[(pX * 2 + 1)-1][(pY*2+1)] = 6;
	if (maze[pX][pY].getRight() != nullptr)
		mazeMapInt[(pX * 2 + 1)][(pY * 2 + 1)+1] = 6;
	if (maze[pX][pY].getDown() != nullptr)
		mazeMapInt[(pX * 2 + 1)+1][(pY * 2 + 1)] = 6;
	if (maze[pX][pY].getLeft() != nullptr)
		mazeMapInt[(pX * 2 + 1)][(pY * 2 + 1)-1] = 6;

}

void moveAttack(int moveDirection, vector<vector<Node>>& maze, Player& p, int &enemyHealth) {
	int pX = p.getX();
	int pY = p.getY();
	movementDirection(pX, pY, moveDirection, maze, true);
	
	if (maze[pX][pY].getEnemy() != nullptr) {
		int enemHealth = maze[pX][pY].getEnemy()->getHealth() - p.getWeapon();

		if (enemHealth > 0) {
			maze[pX][pY].getEnemy()->setHealth(enemHealth);
			enemyHealth = enemHealth;
		}
		else {
			enemyHealth = 0;
			p.weaponUpgrade();

			int points = p.getPoints();
			int enemPoints = maze[pX][pY].getEnemy()->getWinPoints();
			points += enemPoints;
			p.setPoints(points);
			cout << "player points: " << p.getPoints() << endl;
			int giveHealth = enemPoints / 4;
			maze[pX][pY].setBonus(new Bonus(pX, pY, giveHealth, 0));
			maze[pX][pY].setEnemy(nullptr);
			
		}
			
	}
}

void addEnemiesToMap(int enemCount, int mazeSize, vector<Entity*> &ent) {

	vector<vector<int>> freeSpaces; // vector of tuples ??
	for (int i = 1; i < mazeSize; i++) {
		for (int j = 1; j < mazeSize; j++) {

			vector<int> space = { i,j };
			freeSpaces.push_back(space);
		}
	}

	for (int i = 0; i < enemCount; i++) {

		int randNum = rand() % freeSpaces.size();
		vector<int> xNy = freeSpaces[randNum];
		freeSpaces.erase(freeSpaces.begin() + freeSpaces.size() - 1);

		ent.push_back(new Enemy(xNy[0], xNy[1]));
	}

}

void movementDirection(int &pX, int &pY, int moveDirection, vector<vector<Node>>&maze, bool isPlayerMove) {
	int moveCount = 4;
	if (isPlayerMove)
		moveCount = 1;

	for (int i = 0; i < moveCount; i++) {
		moveDirection += i;
		switch (moveDirection) {
			case 1:
				if (maze[pX][pY].getUp() != nullptr) {
					pX -= 1;
					return;
				}

				break;
			case 2:
				if (maze[pX][pY].getRight() != nullptr) {
					pY += 1;
					return;
				}
				break;
			case 3:
				if (maze[pX][pY].getDown() != nullptr) {
					pX += 1;
					return;
				}

				break;
			case 4:
				if (maze[pX][pY].getLeft() != nullptr) {
					pY -= 1;
					return;
				}

				break;
			default:
				break;
		}
	}

}

