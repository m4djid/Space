import java.util.Random;

public class Jeu {

	static int d1;
	static int d2;
	static int d3;
	static int a;
	static int b;
	static int c;
	static int nombreLancer;
	static int njetons1;
	static int njetons2;
	static int njetons;
	static int s;
	static int s1;
	static int s2;
	static int Nj1;
	static int Nj2;

	static void classement(int d1, int d2, int d3)
	{
		if(d1<d2)
		{
			if(d3<d1) 
			{
				a = d2;
				b = d1;
				c = d3;
				return;
			}
			if(d3<d2)
			{
				a = d2;
				b = d3;
				c = d1;
				return;
			}
			else
			{
				a = d3;
				b = d2;
				c = d1;
				return;
			}
		}
		else 
		{
			if(d3<d2)
			{
			a = d1;
			b = d2;
			c = d3;
			return;
			}
			if(d3<d1)
			{
				a = d1;
				b = d3;
				c = d2;
				return;
			}
			else
			{
				a = d3;
				b = d1;
				c = d2;
				return;
			}
		}
	}
	
	static int randomize()
	{
		int dice;
		int maximum = 6;
		int minimum = 1;
		Random rn = new Random();
		int i = Math.abs(rn.nextInt() % 6);
		dice =  minimum + i;
		
		
	return dice;	
	
	}
	
	static boolean tierce(int a, int b, int c) 
	{
		if(c + 1 == b && b + 1 == a)
		{
			return true;
		}
		
		return false;
	}
	
	static boolean brelan(int a, int b, int c)
	{
		if(a==b && b == c)
		{
			return true;
		}
		return false;
	}
	
	static boolean _421(int a, int b, int c)
	{
		if(a==4 && b==2 && c==1)
		{
			return true;
		}
		return false;
	}
	
	static int calculNbreJetons(int a, int b, int c)
	{
		int jetons;
		boolean vtierce = tierce(a,b,c);
		boolean vbrelan = brelan(a,b,c);
		boolean v_421 = _421(a,b,c);
		
		if(v_421 == true)
		{
			return jetons=8;
		}
		if(vbrelan)
		{
			return jetons=5;
		}
		if(vtierce)
		{
			return jetons=2;
		}
		else
		{
			return jetons=1;
		}
	}
	
	static int CalculNbreS(int a, int b, int c)
	{
		int s;
		
		s = (a * 100) + (b *10) + c;
		
		return s;		
	}
	
	static void Tour(int njetonsx, int sx)
	{
		char reponse;
		String relance;
		char garder = 0;
		int numDes;
		int nbDes;
		System.out.println("Début du tour");
		System.out.println("Appuyez sur une touche pour lancer les dés");
		String clavier = Clavier.readString();
		if (clavier !=""){
		d1 = randomize();
		d2 = randomize();
		d3 = randomize();
		System.out.println("d1 "+d1+" d2 "+d2+" d3 "+d3);
		}
		nombreLancer = 1;
		
		System.out.println("Voulez-vous garder la combinaison ? o/n");
		reponse = Clavier.readChar();
		
		
		while(reponse == 'n' && nombreLancer <=3)
		{
			System.out.println("Choisissez le nombre de dés à rejouer");
			nbDes = Clavier.readInt();
			while(nbDes > 3)
			{
				System.out.println("Veuillez choisir au maximum 3 dés");
				nbDes = Clavier.readInt();
			}
			if(nbDes == 1)
			{
				System.out.println("Choisissez le dé à relancer");
				while(nbDes > 3)
				{
					System.out.println("Veuillez choisir un nombre entre 1 et 3");
				}
				numDes = Clavier.readInt();
				if (numDes == 1)
				{
					d1 = randomize();
				}
				else if (numDes == 2)
				{
					d2 = randomize();
				}
				else
				{
					d3 = randomize();
				}
			}
			else if(nbDes ==2)
			{
				System.out.println("Choisissez les dés à relancer");
				while(nbDes == 1 || nbDes > 3)
				{
					System.out.println("Veuillez choisir un nombre inférieur à 3");
				}
				
					int iDes;
					iDes = Clavier.readInt();
				
					if (iDes == 12 || iDes == 21)
					{
						d1 = randomize();
						d2 = randomize();
					}
					else if (iDes == 13 || iDes == 31)
					{
						d1 = randomize();
						d3 = randomize();
					}
					else if (iDes == 23 || iDes == 32)
					{
						d2 = randomize();
						d3 = randomize();
					}
				
			}
			else if (nbDes == 3)
			{
				d1 = randomize();
				d2 = randomize();
				d3 = randomize();
			}
			
			
		System.out.println("Votre nouvelle combinaison : d1 : "+d1+" d2 : "+d2+" d3 : "+d3);	
		nombreLancer = nombreLancer + 1;
		if (nombreLancer <= 3) 
		{
		System.out.println("Voulez-vous garder la combinaison ?");
		reponse = Clavier.readChar();
		}
		}
		classement(d1,d2,d3);
		njetons = calculNbreJetons(a,b,c);
		s = CalculNbreS(a,b,c);
		System.out.println("Fin du tour");
			
	}
	
	static void game() 
	{
		int x;
		System.out.println("Jouez au 421");
		System.out.println("Veuillez entrez un nombre de jeton");
		x = Clavier.readInt();
		njetons = x;
		Nj1 = x;
		Nj2 = x;
		do
		{
		System.out.println("Tour joueur 1");
		Tour(njetons,s);
		njetons1 = njetons;
		s1 = s;
		System.out.println("Tour joueur 2");
		Tour(njetons,s);
		njetons2 = njetons;
		s2 = s;
		
		if (njetons1 == njetons2)
		{
			if(s1 == s2)
			{
				System.out.println("Egalité");
			}
			else if (s1 > s2)
			{
				Nj1 = Nj1 - njetons1;
				Nj2 = Nj2 + njetons1;
				System.out.println("Score :");
				System.out.println("Joueur 1 : "+ Nj1 +" Joueur 2 : "+ Nj2);
			}
			else if (s1 < s2)
			{
				Nj2 = Nj2 - njetons2;
				Nj1 = Nj1 + njetons2;
				System.out.println("Score :");
				System.out.println("Joueur 1 : "+ Nj1 +" Joueur 2 : "+ Nj2);
			}
		}
		else if (njetons1 > njetons2)
		{
			Nj1 = Nj1 - njetons1;
			Nj2 = Nj2 + njetons1;
			System.out.println("Score :");
			System.out.println("Joueur 1 : "+ Nj1 +" Joueur 2 : "+ Nj2);
		}
		else if (njetons1 < njetons2)
		{
			Nj2 = Nj2 - njetons2;
			Nj1 = Nj1 + njetons2;
			System.out.println("Score :");
			System.out.println("Joueur 1 : "+ Nj1 +" Joueur 2 : "+ Nj2);
		}
		if (Nj1 <= 0)
		{
			System.out.println("Joueur 1 a gagné");
		}
		if (Nj2 <= 0)
		{
			System.out.println("Joueur 2 a gagné");
		}
		}
		while (Nj1 > 0 && Nj2 > 0);
	}
	
	
	public static void main(String[] args)
	{
	game();
	}
}
