#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

class Job
{
public:
    string s;    // Job name
    int at, bt, wt, tat, pr, remBT; // Arrival Time, Burst Time, Waiting Time, Turnaround Time, Priority, Remaining Burst Time

    Job()
    {
        s = "";
        at = bt = wt = tat = pr = remBT = 0;
    }

    void getData()
    {
        cout << "Enter Job Name: ";
        cin >> s;
        cout << "Arrival Time: ";
        cin >> at;
        cout << "Burst Time: ";
        cin >> bt;
        remBT = bt;  // Initialize remaining burst time to the burst time
        cout << "Priority: ";
        cin >> pr;
    }
};

void displayTable(const vector<Job> &jobs)
{
    cout << "Job\tAT\tBT\tWT\tTAT\tPR" << endl;
    for (const auto &job : jobs)
    {
        cout << job.s << "\t" << job.at << "\t" << job.bt << "\t" << job.wt << "\t" << job.tat << "\t" << job.pr << endl;
    }
}

// First-Come-First-Served (FCFS) Scheduling
void FCFS(vector<Job> jobs)
{
    cout << "----FCFS Scheduling----" << endl;

 
    sort(jobs.begin(), jobs.end(), [](Job a, Job b) { return a.at < b.at; });
    int time = 0;
    int n = jobs.size();

    for (int i = 0; i < n; i++)
    {
        time = max(time, jobs[i].at);
        jobs[i].wt = time - jobs[i].at;
        jobs[i].tat = jobs[i].wt + jobs[i].bt;
        time += jobs[i].bt;
    }

    displayTable(jobs);
}

// Shortest Job First (Preemptive SJF) Scheduling
void SJF_Preemptive(vector<Job> jobs)
{
    cout << "----Shortest Job First (Preemptive) Scheduling----" << endl;

    int n = jobs.size(), completed = 0, time = 0;
    vector<int> rembt(n); // Remaining burst time
    for (int i = 0; i < n; i++) {
    rembt[i] = jobs[i].bt;

    }


    while (completed < n)
    {
        int idx = -1, minBT = 999;

        for (int i = 0; i < n; i++)
        {
            if (jobs[i].at <= time && rembt[i] > 0 && rembt[i] < minBT)
            {
                idx = i;
                minBT = rembt[i];
            }
        }

        if (idx == -1)
            time++;
        else
        {
            rembt[idx]--;
            time++;
            if (rembt[idx] == 0)
            {
                completed++;
                jobs[idx].tat = time - jobs[idx].at;
                jobs[idx].wt = jobs[idx].tat - jobs[idx].bt;
            }
        }
    }

    displayTable(jobs);
}

// Priority (Non-Preemptive) Scheduling
void Priority(vector<Job> jobs)
{
    cout << "----Priority (Non-Preemptive) Scheduling----" << endl;

    int time = 0;
    vector<Job> completedJobs;

    while (!jobs.empty())
    {
        int idx = -1, minPR = 999;
        for (int i = 0; i < jobs.size(); i++)
        {
            if (jobs[i].at <= time && jobs[i].pr < minPR)
            {
                idx = i;
                minPR = jobs[i].pr;
            }
        }

        if (idx == -1)
            time++;
        else
        {
            jobs[idx].wt = time - jobs[idx].at;
            jobs[idx].tat = jobs[idx].wt + jobs[idx].bt;
            time += jobs[idx].bt;
            completedJobs.push_back(jobs[idx]);
            jobs.erase(jobs.begin() + idx);
        }
    }

    displayTable(completedJobs);
}

void RoundRobin(vector<Job>& jobs, int quantum) {
    cout << "----Round Robin (Preemptive) Scheduling----" << endl;

    int n = jobs.size(), time = 0;
    queue<int> q; // Queue to store job indices
    vector<int> rembt(n); // Remaining burst times
    for (int i = 0; i < n; i++) {
        rembt[i] = jobs[i].bt; // Initialize remaining burst times with burst times
    }

    vector<int> finishTime(n, -1); // To store the completion time for each job
    vector<bool> inQueue(n, false); // Track which jobs are already in the queue

    // Initially, add all jobs that have arrived at time = 0
    for (int i = 0; i < n; i++) {
        if (jobs[i].at <= time) {
            q.push(i);
            inQueue[i] = true;
        }
    }

    while (!q.empty()) {
        int i = q.front();  // Get the first job in the queue
        q.pop();
        inQueue[i] = false;

        // Calculate execution time for the quantum or remaining burst time, whichever is smaller
        int execTime = min(quantum, rembt[i]);
        rembt[i] -= execTime;
        time += execTime;

        // If the job is completed
        if (rembt[i] == 0 && finishTime[i] == -1) {
            finishTime[i] = time; // Set the finish time for the job
        }

        // Add jobs that have arrived during the time interval and are not already in the queue
        for (int j = 0; j < n; j++) {
            if (jobs[j].at <= time && rembt[j] > 0 && !inQueue[j]) {
                q.push(j);
                inQueue[j] = true;
            }
        }

        // If the job is not completed, add it back to the queue
        if (rembt[i] > 0) {
            q.push(i);
            inQueue[i] = true;
        }
    }

    // Calculate Waiting Time (WT) and Turnaround Time (TAT)
    for (int i = 0; i < n; i++) {
        jobs[i].tat = finishTime[i] - jobs[i].at; // Turnaround time = Finish time - Arrival time
        jobs[i].wt = jobs[i].tat - jobs[i].bt;    // Waiting time = Turnaround time - Burst time
    }

    displayTable(jobs); // Display the result
}


int main()
{
    int n;
    cout << "Enter total number of jobs: ";
    cin >> n;

    vector<Job> jobs(n);
    for (int i = 0; i < n; i++)
    {
        cout << "Enter details for Job " << i + 1 << endl;
        jobs[i].getData();
    }

    FCFS(jobs);
    SJF_Preemptive(jobs);
    Priority(jobs);
    int quantum;
    cout << "Enter time quantum for Round Robin: ";
    cin >> quantum;
    RoundRobin(jobs, quantum);

    return 0;
}
