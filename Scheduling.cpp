#include <bits/stdc++.h>
using namespace std;

class Job
{
public:
    string name;
    int arivalT, burstT, waitT, turnarroundT, priority, completionT, remainingBurst;

    Job()
    {
        name = "";
        arivalT = burstT = waitT = turnarroundT = completionT = remainingBurst =0;
    }

    void setData(int bur, int ar, string n, int pr){
        name = n;
        burstT= bur;
        arivalT = ar;
        priority = pr;

    }

    void getData()
    {
        cout << "Name : ";
        cin >> name;
        cout << "Arrival T: ";
        cin >> arivalT;
        cout << "Burst T: ";
        cin >> burstT;
        cout << "Priority: ";
        cin >> priority;
        remainingBurst = burstT;
    }

    void reset(){
        remainingBurst = burstT;
        waitT = completionT = turnarroundT = 0;
    }
};

void Table(vector<Job> v)
{
    cout << "Process \t   Arival Time \t\t   Burst Time \t\t   Priority\t\t   Wait Time \t\t   Turnaround Time \t   Completion Time" << endl;
    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i].name << "\t\t\t" << v[i].arivalT << "\t\t\t" << v[i].burstT << "\t\t\t" << v[i].priority << "\t\t\t" << v[i].waitT << "\t\t\t" << v[i].turnarroundT << "\t\t\t" << v[i].completionT <<endl;
    }
}


void FCFS(vector<Job> v){
    cout << "----FCFS----" << endl;


    sort(v.begin(), v.end(), [](Job a, Job b){
        return a.arivalT < b.arivalT;
    });

    int t = 0;


    for(int i = 0; i < v.size(); i++){
        t = max(t, v[i].arivalT); 

        v[i].completionT = t + v[i].burstT;

        v[i].turnarroundT = v[i].completionT - v[i].arivalT;

        v[i].waitT = v[i].turnarroundT- v[i].burstT;

        t = v[i].completionT;
    }

    Table(v);

}


void PrioityNon(vector<Job> v){

    cout << "---------------------------------------------Priority--------------------------------------------------" << endl;

    int completed = 0;

    int t = 0;

    while(completed < v.size()){

        int idx = -1;
        int MaxPriority = INT_MIN;

        for(int j = 0; j < v.size(); j++){
            if(v[j].arivalT <= t && v[j].priority > MaxPriority && v[j].completionT == 0) {
                idx = j;
                MaxPriority = v[j].priority;
            }
        }

        if(idx == -1){
            t++;
        } else {
            // non premeptive so complte that job

            v[idx].completionT = t + v[idx].burstT;
            v[idx].turnarroundT = v[idx].completionT - v[idx].arivalT;
            v[idx].waitT = v[idx].turnarroundT - v[idx].burstT;

            t = v[idx].completionT;

            completed ++;

        }


    }

    Table(v);


}


void RoundRobinPreEmptive(vector<Job> v, int allocation){

    cout << "-------------------------Round Robin---------------------------------\n";

    queue<Job*> readyQ;

    map<Job*, bool> already;

    for(Job j: v){
        already[&j] = false;
    }

    int completed = 0;

    int t = 0;


    while(completed < v.size()){

        for(int j = 0; j < v.size(); j++){
            if(!already[&v[j]] && v[j].arivalT <= t){ // first condition checks if you have already pushed that guy in the queue
                readyQ.push(&v[j]);
                already[&v[j]] = true;
            }
        }

        if(readyQ.empty()){

            t ++;

        } else {

            Job *b = readyQ.front();
            readyQ.pop();

            if( b->remainingBurst < allocation){
                completed++;
                t = t + b->remainingBurst;
                b->remainingBurst = 0;
                b->completionT = t;
                b->turnarroundT = b->completionT - b->arivalT;
                b->waitT = b->turnarroundT - b->burstT;

            } else {
                b->remainingBurst = b->remainingBurst  - allocation;
                readyQ.push(b);
                t = t + allocation;
            }

        }


    }


    Table(v);



}


void SJFPreEmptive(vector<Job> v){

    cout << "------------------------SJF PreEmptive-------------------------------" << endl;

    int t = 0;


    int compltedJobs = 0;

    vector<string> ganets;

    while(compltedJobs < v.size()){

        // find which process should use current timestamp for execution
        // find the process with shortest remaining burst time remaining at current time stamp
        //

        int indxOfSuch = -1;
        int burstTimeMin = __INT_MAX__;

        for(int i = 0; i < v.size(); i++){

            if(v[i].arivalT < t && v[i].remainingBurst < burstTimeMin && v[i].remainingBurst > 0){ // last condition to check if the process hasnt already been executed to completion
                indxOfSuch = i;
                burstTimeMin = v[i].remainingBurst;
            } 

        }

        if(indxOfSuch == -1){
            // no such process
            ganets.push_back("$");
            t++;

        } else {

            v[indxOfSuch].remainingBurst --;
            ganets.push_back(v[indxOfSuch].name);
            t++;

            if(v[indxOfSuch].remainingBurst == 0){
                compltedJobs ++;

                v[indxOfSuch].completionT = t;
                v[indxOfSuch].turnarroundT = v[indxOfSuch].completionT - v[indxOfSuch].arivalT;
                v[indxOfSuch].waitT = v[indxOfSuch].turnarroundT- v[indxOfSuch].burstT;
            }


        }


    }


    Table(v);

    cout << "\n\n\n\n\n\n\n\n\n\n";

    int x = 0;

    for(int j = 0; j < ganets.size(); j++){
        cout << ganets[j] << "\t";
        x ++;

        if(x >= 16){
            x = 0;
            cout << "\n";
        }
    }
    
}


int main(){

    int num;

    vector<Job> jobs;
    int RoundRobin;

    cout << "ENTER NUMBER OF JOBS: \n";
    cin >> num;

    for(int i = 0; i < num; i++){
        Job b;
        b.getData();
        jobs.push_back(b);
    }

    cout << "\n\n\nEnter Quanta for Round-Robin";
    cin >> RoundRobin;

    cout << "\n\n\n\n";

    // string names[10] = {
    //     "A", "B", "C", "D", "E", "F", "G", "H", "I", "K"
    // };

    // int ar[10] = {
    //     10, 35, 1, 56, 13, 11, 6, 4, 11, 44
    // };

    // int burs[10] = {
    //     19, 26, 22, 19, 22, 30, 18, 33, 1, 22
    // };

    // int p[10] = {
    //     10, 24, 45, 16, 29, 16, 28, 15, 27, 17
    // };

    //RoundRobin = 6;

    // for(int i = 0; i < 10; i++){
    //     Job b;
    //     b.setData(burs[i], ar[i], names[i], p[i]);
    //     jobs.push_back(b);
    // }

    FCFS(jobs);

    for(int i = 0; i < jobs.size(); i++){
        jobs[i].reset();
    }

    SJFPreEmptive(jobs);

    for(int i = 0; i < jobs.size(); i++){
        jobs[i].reset();
    }

    cout << "\n\n\n\n\n\n";

    PrioityNon(jobs);


    for(int i = 0; i < jobs.size(); i++){
        jobs[i].reset();
    }

    cout << "\n\n\n\n\n\n";

    RoundRobinPreEmptive(jobs, RoundRobin);

    return 0;


}
