using System;
using mgraph.Model;
using System.Diagnostics;
using Microsoft.EntityFrameworkCore;
using System.Linq;
using System.Collections.Generic;
using System.Threading;

namespace mgraph
{
    class Program
    {
        public static Random random = new Random();
        public static GraphContext context = new GraphContext();
        public static Stopwatch stopWatch = new Stopwatch();

        static void Main(string[] args)
        {
            context.Database.Migrate();
            //FillDatabase(50000, 5000);
            //Console.ReadLine();
            GenerateMetagraph(10, 10);
            Console.WriteLine("Done!");
            Console.ReadLine();
            //AddMetavertex(50, 10000);
            //Console.ReadLine();
            Console.ReadLine();
        }

        static void AddMetavertex(int test_size, int vertex_size)
        {
            double avg1 = 0;
            double avg2 = 0;
            for (int n = 0; n < test_size; n++)
            {
                stopWatch.Start();

                var children = context.Set<Node>().Include(m => m.Children).Where(m => m.NodeId <= vertex_size);
                var parent = context.Set<Node>().Include(m => m.Children).OrderByDescending(u => u.NodeId).First();

                parent.Children.AddRange(children);
                context.SaveChanges();

                if (n > 0) avg1 += stopWatch.ElapsedTicks;
                PrintTime("+Node MetaVertex");

                stopWatch.Start();

                parent = context.Set<Node>().Include(m => m.Children).OrderByDescending(u => u.NodeId).First();
                parent.Children.Clear();
                context.SaveChanges();

                if (n > 0) avg2 += stopWatch.ElapsedTicks;
                PrintTime("-Node MetaVertex");
            }
            PrintAvg(avg1, test_size - 1, "+Node MetaVertex AVG");
            PrintAvg(avg2, test_size - 1, "-Node MetaVertex AVG");
        }

        static void FillDatabase(int node_count, int save_interval)
        {
            context.ChangeTracker.AutoDetectChangesEnabled = false;

            for (int n = 1; n <= node_count; n++)
            {
                context.Nodes.Add(new Node()
                {
                    Int_value = random.Next(0, 100),
                    Float_value = RandomFloat(0.0, 300.0),
                    String_value = $"v{n}"
                });

                if (n % save_interval == 0)
                {
                    context.SaveChanges();
                }
            }

            for (int n = 1; n <= node_count - 1; n++)
            {
                context.Edges.Add(new Edge()
                {
                    FromNodeId = n,
                    ToNodeId = n + 1
                });

                if (n % save_interval == 0)
                {
                    context.SaveChanges();
                }
            }
            context.SaveChanges();
            context.ChangeTracker.AutoDetectChangesEnabled = true;
        }

        static void GenerateMetagraph(int depth, int child_amount, List<Node> parent_nodes = null)
        {
            if (parent_nodes == null)
            {
                var parents = new List<Node>();
                for (int i = 0; i < child_amount; i++)
                {
                    Node parent = new Node()
                    {
                        Int_value = random.Next(0, 100),
                        Float_value = RandomFloat(0.0, 300.0),
                        String_value = $"v{i}_{depth}"
                    };
                    parents.Add(parent);
                }
                context.Nodes.AddRange(parents);
                context.SaveChanges();
                Console.WriteLine($"Generated {depth} level");
                GenerateMetagraph(depth - 1, child_amount, parents);
                return;
            }

            foreach (Node parent_node in parent_nodes)
            {
                var children = new List<Node>();
                for (int i = 0; i < child_amount; i++)
                {
                    children.Add(new Node()
                    {
                        Int_value = random.Next(0, 100),
                        Float_value = RandomFloat(0.0, 300.0),
                        String_value = $"v{i}_{depth}",
                        ParentNode = parent_node
                    });
                }
                context.Nodes.AddRange(children);
                context.SaveChanges();
                Console.WriteLine($"Generated {depth} level");
                if (depth > 1) GenerateMetagraph(depth - 1, child_amount, children);
            }
        }

        static void PrintTime(string str)
        {
            stopWatch.Stop();
            double ticks = stopWatch.ElapsedTicks;
            double seconds = ticks / Stopwatch.Frequency;
            double milliseconds = (ticks / Stopwatch.Frequency) * 1000;
            double nanoseconds = (ticks / Stopwatch.Frequency) * 1000000000;
            int indent = $"{str}".Length;
            Console.WriteLine($"{str}{new String(' ', 30 - indent)}{seconds}s {milliseconds}ms {nanoseconds}ns");
            stopWatch.Reset();
        }

        static void PrintAvg(double ticks, int test_size, string str)
        {
            ticks = ticks / test_size;
            double seconds = ticks / Stopwatch.Frequency;
            double milliseconds = (ticks / Stopwatch.Frequency) * 1000;
            double nanoseconds = (ticks / Stopwatch.Frequency) * 1000000000;
            int indent = $"{str}".Length;
            Console.WriteLine($"{str}{new String(' ', 30 - indent)}{seconds}s {milliseconds}ms {nanoseconds}ns");
        }

        static void RemoveAllNodes(List<Node> nodes)
        {
            foreach (var node in nodes)
            {
                RemoveAllNodes(node.Children);
            };
            context.Nodes.RemoveRange(nodes);
        }

        static float RandomFloat(double one, double two)
        {
            Random rand = new Random();
            return Convert.ToSingle(one + rand.NextDouble() * (two - one));
        }
    }
}
