import java.io.*;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;

public class Clavier
{

    private static BufferedReader in;
    private static StringTokenizer epelleur = new StringTokenizer("");

    private static void afficher(String s)
    {
        if(s != null)
        {
            System.out.print(s);
            System.out.flush();
        }
    }

    private Clavier()
    {
    }

    private static String getString()
    {
        try
        {
            return in.readLine();
        }
        catch(IOException ioexception)
        {
            return "";
        }
    }

    private static void miseAJourEpelleur()
    {
        for(; 0 == epelleur.countTokens(); epelleur = new StringTokenizer(getString())) { }
    }

    public static String readString()
    {
        miseAJourEpelleur();
        try
        {
            return epelleur.nextToken();
        }
        catch(NoSuchElementException nosuchelementexception)
        {
            return "";
        }
    }

    public static String readString(String s)
    {
        afficher(s);
        return readString();
    }

    public static int readInt()
    {
        return (int)readLong();
    }

    public static int readInt(String s)
    {
        return (int)readLong(s);
    }

    public static int readInt(int i, int j)
    {
        return (int)readLong(i, j);
    }

    public static int readInt(String s, int i, int j)
    {
        return (int)readLong(s, i, j);
    }

    public static long readLong()
    {
        return readLong(null);
    }

    public static long readLong(String s)
    {
        try
        {
            return Long.parseLong(readString(s));
        }
        catch(NumberFormatException numberformatexception)
        {
            System.out.println("Erreur. Donnez un entier : ");
        }
        return readLong();
    }

    public static long readLong(long l, long l1)
    {
        return readLong(null, l, l1);
    }

    public static long readLong(String s, long l, long l1)
    {
        long l2 = readLong(s);
        if(l <= l2 && l2 <= l1)
        {
            return l2;
        } else
        {
            System.out.println("Erreur. Donnez une valeur entre " + l + " et " + l1 + " :");
            return readLong(l, l1);
        }
    }

    public static double readDouble()
    {
        return readDouble(null);
    }

    public static double readDouble(String s)
    {
        try
        {
            return Double.parseDouble(readString(s));
        }
        catch(NumberFormatException numberformatexception)
        {
            System.out.println("Erreur. Donnez un double : ");
        }
        return readDouble();
    }

    public static double readDouble(double d, double d1)
    {
        return readDouble(null, d, d1);
    }

    public static double readDouble(String s, double d, double d1)
    {
        double d2 = readDouble(s);
        if(d <= d2 && d2 <= d1)
        {
            return d2;
        } else
        {
            System.out.println("Erreur. Donnez une valeur entre " + d + " et " + d1 + " :");
            return readDouble(d, d1);
        }
    }

    public static float readFloat()
    {
        return readFloat(null);
    }

    public static float readFloat(String s)
    {
        try
        {
            return Float.parseFloat(readString(s));
        }
        catch(NumberFormatException numberformatexception)
        {
            System.out.println("Erreur. Donnez un float : ");
        }
        return readFloat();
    }

    public static float readFloat(float f, float f1)
    {
        return readFloat(null, f, f1);
    }

    public static float readFloat(String s, float f, float f1)
    {
        float f2 = readFloat(s);
        if(f <= f2 && f2 <= f1)
        {
            return f2;
        } else
        {
            System.out.println("Erreur. Donnez une valeur entre " + f + " et " + f1 + " :");
            return readFloat(f, f1);
        }
    }

    public static char readChar()
    {
        return readChar(null);
    }

    public static char readChar(String s)
    {
        return readString(s).charAt(0);
    }

    public static char readChar(char c, char c1)
    {
        return readChar(null, c, c1);
    }

    public static char readChar(String s, char c, char c1)
    {
        char c2 = readChar(s);
        if(c <= c2 && c2 <= c1)
        {
            return c2;
        } else
        {
            System.out.println("Erreur. Donnez une valeur entre " + c + " et " + c1 + " :");
            return readChar(c, c1);
        }
    }

    static 
    {
        in = new BufferedReader(new InputStreamReader(System.in));
    }
}