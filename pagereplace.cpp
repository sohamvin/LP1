#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class PageReplacement
{
private:
    int n;
    int f;

    vector<int> pages;
    vector<int> frames;

    int Faults = 0;
    int Hits = 0;

    void initialize()
    {
        Faults = 0;
        Hits = 0;

        frames.assign(n, 999);
    }

    bool isHit(int data)
    {
        for (int i = 0; i < f; i++)
        {
            if (frames[i] == data)
            {
                return true;
            }
        }
        return false;
    }

    void DisplayPages()
    {
        for (int i = 0; i < f; i++)
        {
            if (frames[i] != 999)
            {
                cout << frames[i] << " ";
            }
        }
        cout << endl;
    }

    void DisplayFaultsHits()
    {
        cout << "Page Faults: " << Faults << endl;
        cout << "Page Hits: " << Hits << endl;
    }

public:
    void getData()
    {
        cout << "Total Pages: ";
        cin >> n;

        cout << "Enter the page reference sequence: ";

        for (int i = 0; i < n; i++)
        {
            int x;
            cin >> x;
            pages.push_back(x);
        }

        cout << "Frame Size: ";
        cin >> f;

        frames.resize(f);
    }

    void FIFO()
    {
        cout << "------ FIFO Algorithm ------" << endl
             << endl;

        initialize();

        for (int i = 0; i < n ; i++)
        {
            cout << "For " << pages[i] << " : ";

            if (!isHit(pages[i]))
            {
                Faults++;
                for (int j = 0; j < f - 1; j++)
                {
                    frames[j] = frames[j + 1];
                }
                frames[f - 1] = pages[i];
                DisplayPages();
            }
            else
            {
                Hits++;
                cout << "No page Fault" << endl;
            }
        }

        DisplayFaultsHits();
    }

    void Optimal()
    {
        cout << "------ Optimal Algorithm ------" << endl
             << endl;

        initialize();

        vector<int> indexes(f, 0);

        for (int i = 0; i < n; i++)
        {
            cout << "For " << pages[i] << " : ";

            if (!isHit(pages[i]))
            {
                Faults++;
                for (int j = 0; j < f; j++)
                {
                    int pg = frames[j];
                    bool found = false;

                    for (int k = i; k < n; k++)
                    {
                        if (pg == pages[k])
                        {
                            indexes[j] = k;
                            found = true;
                            break;
                        }
                    }

                    if (!found)
                    {
                        indexes[j] = 999;
                    }
                }

                int max = -1;

                int ind;

                for (int j = 0; j < f; j++)
                {
                    if (indexes[j] > max)
                    {
                        max = indexes[j];
                        ind = j;
                    }
                }

                frames[ind] = pages[i];
                DisplayPages();
            }
            else
            {
                Hits++;
                cout << "No page Fault" << endl;
            }
        }

        DisplayFaultsHits();
    }

    void LRU()
    {
        cout << "------ LRU Algorithm ------" << endl
             << endl;

        initialize();

        vector<int> indexes(f, 0);

        for (int i = 0; i < n; i++)
        {
            cout << "For " << pages[i] << " : ";

            if (!isHit(pages[i]))
            {
                Faults++;
                for (int j = 0; j < f; j++)
                {
                    int pg = frames[j];
                    bool found = false;

                    for (int k = i - 1; k >= 0; k--)
                    {
                        if (pg == pages[k])
                        {
                            indexes[j] = k;
                            found = true;
                            break;
                        }
                    }

                    if (!found)
                    {
                        indexes[j] = -9999;
                    }
                }

                int min = 9999;

                int ind;

                for (int j = 0; j < f; j++)
                {
                    if (indexes[j] < min)
                    {
                        min = indexes[j];
                        ind = j;
                    }
                }

                frames[ind] = pages[i];
                DisplayPages();
            }
            else
            {
                Hits++;
                cout << "No page Fault" << endl;
            }
        }

        DisplayFaultsHits();
    }
};

int main()
{
    PageReplacement p;

    p.getData();

    p.FIFO();

    p.Optimal();

    p.LRU();

    return 0;
}