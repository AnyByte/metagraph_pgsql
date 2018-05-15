using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using System;
using System.Collections.Generic;

namespace mgraph.Migrations
{
    public partial class initial : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.EnsureSchema(
                name: "public");

            migrationBuilder.CreateTable(
                name: "Nodes",
                schema: "public",
                columns: table => new
                {
                    NodeId = table.Column<int>(nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn),
                    Float_value = table.Column<float>(nullable: false),
                    Int_value = table.Column<int>(nullable: false),
                    ParentNodeId = table.Column<int>(nullable: true),
                    String_value = table.Column<string>(nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Nodes", x => x.NodeId);
                    table.ForeignKey(
                        name: "FK_Nodes_Nodes_ParentNodeId",
                        column: x => x.ParentNodeId,
                        principalSchema: "public",
                        principalTable: "Nodes",
                        principalColumn: "NodeId",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "Edges",
                schema: "public",
                columns: table => new
                {
                    EdgeId = table.Column<int>(nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn),
                    FromNodeId = table.Column<int>(nullable: false),
                    ParentEdgeId = table.Column<int>(nullable: true),
                    ToNodeId = table.Column<int>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Edges", x => x.EdgeId);
                    table.ForeignKey(
                        name: "FK_Edges_Nodes_FromNodeId",
                        column: x => x.FromNodeId,
                        principalSchema: "public",
                        principalTable: "Nodes",
                        principalColumn: "NodeId",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Edges_Edges_ParentEdgeId",
                        column: x => x.ParentEdgeId,
                        principalSchema: "public",
                        principalTable: "Edges",
                        principalColumn: "EdgeId",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Edges_Nodes_ToNodeId",
                        column: x => x.ToNodeId,
                        principalSchema: "public",
                        principalTable: "Nodes",
                        principalColumn: "NodeId",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Edges_FromNodeId",
                schema: "public",
                table: "Edges",
                column: "FromNodeId");

            migrationBuilder.CreateIndex(
                name: "IX_Edges_ParentEdgeId",
                schema: "public",
                table: "Edges",
                column: "ParentEdgeId");

            migrationBuilder.CreateIndex(
                name: "IX_Edges_ToNodeId",
                schema: "public",
                table: "Edges",
                column: "ToNodeId");

            migrationBuilder.CreateIndex(
                name: "IX_Nodes_ParentNodeId",
                schema: "public",
                table: "Nodes",
                column: "ParentNodeId");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Edges",
                schema: "public");

            migrationBuilder.DropTable(
                name: "Nodes",
                schema: "public");
        }
    }
}
