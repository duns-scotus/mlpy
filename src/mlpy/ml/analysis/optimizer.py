"""
Optimizer - Phase 3 Pipeline Stage

Code optimization passes for performance enhancement and code quality improvement.
Performs dead code elimination, constant folding, and other optimizations.
"""

from typing import Dict, List, Optional, Set, Any, Union
from dataclasses import dataclass
from enum import Enum
import copy

from ..grammar.ast_nodes import (
    ASTNode, Program, FunctionDefinition, AssignmentStatement,
    BinaryExpression, UnaryExpression, FunctionCall, Identifier,
    Literal, NumberLiteral, StringLiteral, BooleanLiteral,
    ArrayLiteral, ObjectLiteral, IfStatement, WhileStatement,
    ForStatement, ReturnStatement, BlockStatement
)

from .type_checker import TypeInfo, MLType


class OptimizationType(Enum):
    """Types of optimizations performed."""
    CONSTANT_FOLDING = "constant_folding"
    DEAD_CODE_ELIMINATION = "dead_code_elimination"
    REDUNDANT_ASSIGNMENT = "redundant_assignment"
    LOOP_OPTIMIZATION = "loop_optimization"
    FUNCTION_INLINING = "function_inlining"
    EXPRESSION_SIMPLIFICATION = "expression_simplification"


@dataclass
class OptimizationResult:
    """Result of a single optimization."""
    optimization_type: OptimizationType
    description: str
    node_before: ASTNode
    node_after: Optional[ASTNode]  # None if node was eliminated
    performance_impact: str  # "high", "medium", "low"


@dataclass
class OptimizerResult:
    """Result of optimization analysis."""
    optimized_ast: ASTNode
    optimizations_applied: List[OptimizationResult]
    optimization_time_ms: float
    nodes_before: int
    nodes_after: int
    estimated_performance_gain: float  # Percentage improvement estimate

    @property
    def optimization_summary(self) -> Dict[OptimizationType, int]:
        """Get count of optimizations by type."""
        summary = {}
        for opt in self.optimizations_applied:
            if opt.optimization_type not in summary:
                summary[opt.optimization_type] = 0
            summary[opt.optimization_type] += 1
        return summary

    @property
    def nodes_eliminated(self) -> int:
        """Get number of nodes eliminated."""
        return self.nodes_before - self.nodes_after


class MLOptimizer:
    """
    Code optimizer for ML language with performance enhancement passes.

    Optimization Passes:
    1. Constant folding - Evaluate constant expressions at compile time
    2. Dead code elimination - Remove unreachable or unused code
    3. Redundant assignment elimination - Remove unnecessary assignments
    4. Expression simplification - Simplify complex expressions
    5. Loop optimization - Optimize loop constructs
    6. Function inlining - Inline simple functions (limited)
    """

    def __init__(self):
        self.optimizations: List[OptimizationResult] = []
        self.symbol_table: Dict[str, Any] = {}
        self.constant_values: Dict[str, Any] = {}
        self.used_variables: Set[str] = set()
        self.reachable_code: Set[ASTNode] = set()

    def optimize(self, ast: ASTNode, type_info: Dict[ASTNode, TypeInfo] = None) -> OptimizerResult:
        """
        Perform comprehensive optimization on the AST.

        Args:
            ast: Root AST node to optimize
            type_info: Type information from type checking stage

        Returns:
            OptimizerResult with optimized AST and optimization details
        """
        import time
        start_time = time.perf_counter()

        # Reset optimizer state
        self.optimizations = []
        self.symbol_table = {}
        self.constant_values = {}
        self.used_variables = set()
        self.reachable_code = set()

        # Count nodes before optimization
        nodes_before = self._count_nodes(ast)

        # Deep copy AST to avoid modifying original
        optimized_ast = copy.deepcopy(ast)

        # Perform optimization passes
        optimized_ast = self._pass_1_constant_folding(optimized_ast)
        optimized_ast = self._pass_2_dead_code_elimination(optimized_ast)
        optimized_ast = self._pass_3_expression_simplification(optimized_ast)
        optimized_ast = self._pass_4_redundant_assignment_elimination(optimized_ast)
        optimized_ast = self._pass_5_loop_optimization(optimized_ast)

        # Count nodes after optimization
        nodes_after = self._count_nodes(optimized_ast)

        optimization_time_ms = (time.perf_counter() - start_time) * 1000

        # Estimate performance gain
        performance_gain = self._estimate_performance_gain()

        return OptimizerResult(
            optimized_ast=optimized_ast,
            optimizations_applied=self.optimizations.copy(),
            optimization_time_ms=optimization_time_ms,
            nodes_before=nodes_before,
            nodes_after=nodes_after,
            estimated_performance_gain=performance_gain
        )

    def _pass_1_constant_folding(self, ast: ASTNode) -> ASTNode:
        """Pass 1: Constant folding - evaluate constant expressions."""
        return self._constant_fold_node(ast)

    def _pass_2_dead_code_elimination(self, ast: ASTNode) -> ASTNode:
        """Pass 2: Dead code elimination - remove unreachable code."""
        self._mark_reachable_code(ast)
        return self._eliminate_dead_code(ast)

    def _pass_3_expression_simplification(self, ast: ASTNode) -> ASTNode:
        """Pass 3: Expression simplification - simplify complex expressions."""
        return self._simplify_expressions(ast)

    def _pass_4_redundant_assignment_elimination(self, ast: ASTNode) -> ASTNode:
        """Pass 4: Redundant assignment elimination."""
        return self._eliminate_redundant_assignments(ast)

    def _pass_5_loop_optimization(self, ast: ASTNode) -> ASTNode:
        """Pass 5: Loop optimization."""
        return self._optimize_loops(ast)

    def _constant_fold_node(self, node: ASTNode) -> ASTNode:
        """Perform constant folding on a node."""
        if node is None:
            return None

        # First, recursively optimize children
        node = self._constant_fold_children(node)

        # Then optimize this node
        if isinstance(node, BinaryExpression):
            return self._constant_fold_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self._constant_fold_unary_expression(node)

        return node

    def _constant_fold_binary_expression(self, node: BinaryExpression) -> ASTNode:
        """Constant fold binary expressions."""
        if not (hasattr(node, 'left') and hasattr(node, 'right') and hasattr(node, 'operator')):
            return node

        left = node.left
        right = node.right
        operator = node.operator

        # Check if both operands are literals
        if self._is_constant_literal(left) and self._is_constant_literal(right):
            left_val = self._get_literal_value(left)
            right_val = self._get_literal_value(right)

            if left_val is not None and right_val is not None:
                result = self._evaluate_binary_operation(left_val, operator, right_val)
                if result is not None:
                    # Create optimized literal node
                    optimized_node = self._create_literal_node(result)

                    self._add_optimization(
                        OptimizationType.CONSTANT_FOLDING,
                        f"Folded constant expression: {left_val} {operator} {right_val} = {result}",
                        node,
                        optimized_node,
                        "medium"
                    )

                    return optimized_node

        return node

    def _constant_fold_unary_expression(self, node: UnaryExpression) -> ASTNode:
        """Constant fold unary expressions."""
        if not (hasattr(node, 'operand') and hasattr(node, 'operator')):
            return node

        operand = node.operand
        operator = node.operator

        if self._is_constant_literal(operand):
            operand_val = self._get_literal_value(operand)
            if operand_val is not None:
                result = self._evaluate_unary_operation(operator, operand_val)
                if result is not None:
                    optimized_node = self._create_literal_node(result)

                    self._add_optimization(
                        OptimizationType.CONSTANT_FOLDING,
                        f"Folded constant expression: {operator}{operand_val} = {result}",
                        node,
                        optimized_node,
                        "medium"
                    )

                    return optimized_node

        return node

    def _mark_reachable_code(self, node: ASTNode):
        """Mark all reachable code nodes."""
        if node is None or node in self.reachable_code:
            return

        self.reachable_code.add(node)

        # Mark children as reachable
        if isinstance(node, IfStatement):
            # Always mark condition and then branch as reachable
            if hasattr(node, 'condition'):
                self._mark_reachable_code(node.condition)
            if hasattr(node, 'then_statement'):
                self._mark_reachable_code(node.then_statement)

            # Mark else branch as reachable (even if condition is constant)
            if hasattr(node, 'else_statement') and node.else_statement:
                self._mark_reachable_code(node.else_statement)

        elif isinstance(node, WhileStatement):
            if hasattr(node, 'condition'):
                self._mark_reachable_code(node.condition)
            if hasattr(node, 'body'):
                self._mark_reachable_code(node.body)

        else:
            # Mark all children as reachable
            self._mark_children_reachable(node)

    def _eliminate_dead_code(self, node: ASTNode) -> ASTNode:
        """Eliminate dead (unreachable) code."""
        if node is None:
            return None

        if node not in self.reachable_code:
            self._add_optimization(
                OptimizationType.DEAD_CODE_ELIMINATION,
                f"Eliminated dead code: {type(node).__name__}",
                node,
                None,  # Node eliminated
                "high"
            )
            return None

        # Process children
        node = self._eliminate_dead_code_children(node)
        return node

    def _simplify_expressions(self, node: ASTNode) -> ASTNode:
        """Simplify expressions for better performance."""
        if node is None:
            return None

        # First process children
        node = self._simplify_children(node)

        # Then simplify this node
        if isinstance(node, BinaryExpression):
            return self._simplify_binary_expression(node)

        return node

    def _simplify_binary_expression(self, node: BinaryExpression) -> ASTNode:
        """Simplify binary expressions."""
        if not hasattr(node, 'operator'):
            return node

        operator = node.operator
        left = node.left
        right = node.right

        # Simplification rules
        if operator == '+':
            # x + 0 = x
            if self._is_zero(right):
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified addition with zero",
                    node,
                    left,
                    "low"
                )
                return left
            # 0 + x = x
            elif self._is_zero(left):
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified addition with zero",
                    node,
                    right,
                    "low"
                )
                return right

        elif operator == '*':
            # x * 1 = x
            if self._is_one(right):
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified multiplication by one",
                    node,
                    left,
                    "low"
                )
                return left
            # 1 * x = x
            elif self._is_one(left):
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified multiplication by one",
                    node,
                    right,
                    "low"
                )
                return right
            # x * 0 = 0
            elif self._is_zero(right):
                zero_node = NumberLiteral(value=0)
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified multiplication by zero",
                    node,
                    zero_node,
                    "medium"
                )
                return zero_node
            # 0 * x = 0
            elif self._is_zero(left):
                zero_node = NumberLiteral(value=0)
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified multiplication by zero",
                    node,
                    zero_node,
                    "medium"
                )
                return zero_node

        elif operator == '-':
            # x - 0 = x
            if self._is_zero(right):
                self._add_optimization(
                    OptimizationType.EXPRESSION_SIMPLIFICATION,
                    "Simplified subtraction by zero",
                    node,
                    left,
                    "low"
                )
                return left

        return node

    def _eliminate_redundant_assignments(self, node: ASTNode) -> ASTNode:
        """Eliminate redundant assignments."""
        if node is None:
            return None

        # Process children first
        node = self._eliminate_redundant_assignments_children(node)

        if isinstance(node, AssignmentStatement):
            # Check for redundant assignments like x = x
            if (hasattr(node, 'target') and hasattr(node, 'value') and
                isinstance(node.target, Identifier) and isinstance(node.value, Identifier)):

                if (hasattr(node.target, 'name') and hasattr(node.value, 'name') and
                    node.target.name == node.value.name):

                    self._add_optimization(
                        OptimizationType.REDUNDANT_ASSIGNMENT,
                        f"Eliminated redundant assignment: {node.target.name} = {node.value.name}",
                        node,
                        None,
                        "medium"
                    )
                    return None

        return node

    def _optimize_loops(self, node: ASTNode) -> ASTNode:
        """Optimize loop constructs."""
        if node is None:
            return None

        # Process children first
        node = self._optimize_loops_children(node)

        if isinstance(node, ForStatement):
            # Check for empty loops that can be eliminated
            if hasattr(node, 'body') and self._is_empty_block(node.body):
                self._add_optimization(
                    OptimizationType.LOOP_OPTIMIZATION,
                    "Eliminated empty for loop",
                    node,
                    None,
                    "high"
                )
                return None

        elif isinstance(node, WhileStatement):
            # Check for while(false) loops that can be eliminated
            if (hasattr(node, 'condition') and
                isinstance(node.condition, BooleanLiteral) and
                hasattr(node.condition, 'value') and
                not node.condition.value):

                self._add_optimization(
                    OptimizationType.LOOP_OPTIMIZATION,
                    "Eliminated while(false) loop",
                    node,
                    None,
                    "high"
                )
                return None

        return node

    # Helper methods
    def _count_nodes(self, node: ASTNode) -> int:
        """Count total nodes in AST."""
        if node is None:
            return 0

        count = 1
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    count += self._count_nodes(attr_value)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            count += self._count_nodes(item)
        return count

    def _constant_fold_children(self, node: ASTNode) -> ASTNode:
        """Recursively constant fold child nodes."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    setattr(node, attr_name, self._constant_fold_node(attr_value))
                elif isinstance(attr_value, list):
                    new_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            folded_item = self._constant_fold_node(item)
                            if folded_item is not None:
                                new_list.append(folded_item)
                        else:
                            new_list.append(item)
                    setattr(node, attr_name, new_list)
        return node

    def _mark_children_reachable(self, node: ASTNode):
        """Mark all child nodes as reachable."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    self._mark_reachable_code(attr_value)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            self._mark_reachable_code(item)

    def _eliminate_dead_code_children(self, node: ASTNode) -> ASTNode:
        """Eliminate dead code in children."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    setattr(node, attr_name, self._eliminate_dead_code(attr_value))
                elif isinstance(attr_value, list):
                    new_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            processed_item = self._eliminate_dead_code(item)
                            if processed_item is not None:
                                new_list.append(processed_item)
                        else:
                            new_list.append(item)
                    setattr(node, attr_name, new_list)
        return node

    def _simplify_children(self, node: ASTNode) -> ASTNode:
        """Simplify child expressions."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    setattr(node, attr_name, self._simplify_expressions(attr_value))
                elif isinstance(attr_value, list):
                    new_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            simplified_item = self._simplify_expressions(item)
                            if simplified_item is not None:
                                new_list.append(simplified_item)
                        else:
                            new_list.append(item)
                    setattr(node, attr_name, new_list)
        return node

    def _eliminate_redundant_assignments_children(self, node: ASTNode) -> ASTNode:
        """Eliminate redundant assignments in children."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    setattr(node, attr_name, self._eliminate_redundant_assignments(attr_value))
                elif isinstance(attr_value, list):
                    new_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            processed_item = self._eliminate_redundant_assignments(item)
                            if processed_item is not None:
                                new_list.append(processed_item)
                        else:
                            new_list.append(item)
                    setattr(node, attr_name, new_list)
        return node

    def _optimize_loops_children(self, node: ASTNode) -> ASTNode:
        """Optimize loops in children."""
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['accept', 'line', 'column']:
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, ASTNode):
                    setattr(node, attr_name, self._optimize_loops(attr_value))
                elif isinstance(attr_value, list):
                    new_list = []
                    for item in attr_value:
                        if isinstance(item, ASTNode):
                            optimized_item = self._optimize_loops(item)
                            if optimized_item is not None:
                                new_list.append(optimized_item)
                        else:
                            new_list.append(item)
                    setattr(node, attr_name, new_list)
        return node

    def _is_constant_literal(self, node: ASTNode) -> bool:
        """Check if node is a constant literal."""
        return isinstance(node, (NumberLiteral, StringLiteral, BooleanLiteral))

    def _get_literal_value(self, node: ASTNode) -> Any:
        """Get value from literal node."""
        if hasattr(node, 'value'):
            return node.value
        return None

    def _evaluate_binary_operation(self, left: Any, operator: str, right: Any) -> Any:
        """Evaluate binary operation on constant values."""
        try:
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                if right == 0:
                    return None  # Avoid division by zero
                return left / right
            elif operator == '%':
                if right == 0:
                    return None
                return left % right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '>':
                return left > right
            elif operator == '<=':
                return left <= right
            elif operator == '>=':
                return left >= right
            elif operator == '&&' or operator == 'and':
                return left and right
            elif operator == '||' or operator == 'or':
                return left or right
        except:
            return None
        return None

    def _evaluate_unary_operation(self, operator: str, operand: Any) -> Any:
        """Evaluate unary operation on constant value."""
        try:
            if operator == '-':
                return -operand
            elif operator == '!' or operator == 'not':
                return not operand
            elif operator == '+':
                return +operand
        except:
            return None
        return None

    def _create_literal_node(self, value: Any) -> ASTNode:
        """Create appropriate literal node for value."""
        if isinstance(value, (int, float)):
            return NumberLiteral(value=value)
        elif isinstance(value, str):
            return StringLiteral(value=value)
        elif isinstance(value, bool):
            return BooleanLiteral(value=value)
        else:
            return NumberLiteral(value=0)  # Fallback

    def _is_zero(self, node: ASTNode) -> bool:
        """Check if node represents zero."""
        return (isinstance(node, NumberLiteral) and
                hasattr(node, 'value') and
                node.value == 0)

    def _is_one(self, node: ASTNode) -> bool:
        """Check if node represents one."""
        return (isinstance(node, NumberLiteral) and
                hasattr(node, 'value') and
                node.value == 1)

    def _is_empty_block(self, node: ASTNode) -> bool:
        """Check if node is an empty block or statement."""
        if isinstance(node, BlockStatement):
            return not hasattr(node, 'statements') or not node.statements
        return False

    def _estimate_performance_gain(self) -> float:
        """Estimate performance gain from optimizations."""
        total_gain = 0.0

        for opt in self.optimizations:
            if opt.performance_impact == "high":
                total_gain += 5.0
            elif opt.performance_impact == "medium":
                total_gain += 2.0
            elif opt.performance_impact == "low":
                total_gain += 1.0

        # Cap at reasonable percentage
        return min(total_gain, 50.0)

    def _add_optimization(
        self,
        opt_type: OptimizationType,
        description: str,
        node_before: ASTNode,
        node_after: Optional[ASTNode],
        performance_impact: str
    ):
        """Add an optimization result."""
        optimization = OptimizationResult(
            optimization_type=opt_type,
            description=description,
            node_before=node_before,
            node_after=node_after,
            performance_impact=performance_impact
        )
        self.optimizations.append(optimization)