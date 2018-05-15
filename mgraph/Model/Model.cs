using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;


namespace mgraph.Model
{
    public class Node
    {
        public int NodeId { get; set; }
        public int Int_value { get; set; }
        public float Float_value { get; set; }
        public string String_value { get; set; }

        [ForeignKey("ParentNode")]
        public int? ParentNodeId { get; set; }
        public virtual Node ParentNode { get; set; }
        public virtual List<Node> Children { get; set; }

        public virtual List<Edge> InEdges { get; set; }
        public virtual List<Edge> OutEdges { get; set; }
    }

    public class Edge
    {
        public int EdgeId { get; set; }
        public int FromNodeId { get; set; }
        public int ToNodeId { get; set; }

        [ForeignKey("ParentEdge")]
        public int? ParentEdgeId { get; set; }
        public virtual Edge ParentEdge { get; set; }
        public virtual List<Edge> Children { get; set; }

        public virtual Node FromNode { get; set; }
        public virtual Node ToNode { get; set; }
    }

    public class GraphContext : DbContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=mgraph;Username=maxavatar;Password=1234");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.HasDefaultSchema("public");
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Edge>()
                        .HasOne(m => m.FromNode)
                        .WithMany(t => t.InEdges)
                        .HasForeignKey(m => m.FromNodeId)
                        .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Edge>()
                        .HasOne(m => m.ToNode)
                        .WithMany(t => t.OutEdges)
                        .HasForeignKey(m => m.ToNodeId)
                        .OnDelete(DeleteBehavior.Restrict);
        }

        public DbSet<Node> Nodes { get; set; }
        public DbSet<Edge> Edges { get; set; }
    }
}
