# -*- coding: utf-8 -*-
"""
Test pytextit
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from pytexit import py2tex, uprint


def test_py2tex(verbose=True, **kwargs):
    """
    Note : for debugging use
        pt = ast.parse(expr)
        print(ast.dump(pt))
    """

    # Tests
    expr_py = [
        r"Re_x=(rho*v*x)/mu",
        r"2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2",
        r"f(x**2/y**3)",
        r"arctanh(x/sqrt(x))",
        r"quad(f,0,np.inf)",
        # ------------------
        r"1<2<a<=5",
        r"np.std([f(i) for i in range(21)])",
        r"np.sum([i**2 for i in range(1,101)])==338350",
        r"(a**b)**c",
        r"-x**2",
        r"-(x**2+y**2)",
        r"-(x+y)**2",
        r"(3/4)" + "/" + "(8/15)",
        r"a-(b-(c-d))",
        r"a=(x+y)-(x-y)",
        r"d=(x+y)+(a-b)-(p+q)",
        r"b=-(3*x-2*y)",
        r"c=-(-4*x+5*y)",
    ]

    expr_tex = [
        r"$$Re_x=\frac{\rho v x}{\mu}$$",
        r"$$2\sqrt{\frac{2\pi k T_e}{m_e}} \left(\frac{\Delta E}{k T_e}\right)^2 {a_0}^2$$",
        r"$$f{\left(\frac{x^2}{y^3}\right)}$$",
        r"$$\tanh^{-1}\left(\frac{x}{\sqrt{x}}\right)$$",
        r"$$\int_{0}^{\infty} f\left(u\right) du$$",
        # -------------------
        r"$$1<2<a<=5$$",
        r"$$\operatorname{std}\left(f{\left(i\right)}, i=0..20\right)$$",
        r"$$\sum_{i=1}^{100} i^2=338350$$",
        r"$$\left(a^b\right)^c$$",
        r"$$-x^2$$",
        r"$$-\left(x^2+y^2\right)$$",
        r"$$-\left(x+y\right)^2$$",
        r"$$\frac{\frac{3}{4}}{\frac{8}{15}}$$",
        r"$$a-\left(b-\left(c-d\right)\right)$$",
        r"$$a=x+y-\left(x-y\right)$$",
        r"$$d=x+y+a-b-\left(p+q\right)$$",
        r"$$b=-\left(3x-2y\right)$$",
        r"$$c=-\left(-4x+5y\right)$$",
    ]

    for i, expr in enumerate(expr_py):
        if verbose:
            uprint("")
            uprint("ˆ")
            uprint("Python formula to convert: {0}".format(expr))
            s = py2tex(expr)
            uprint("Got:")
            b = expr_tex[i] == s
            print(s)
            #            uprint('.. correct =', b)
            if not b:
                uprint("Expected:\n", expr_tex[i])
                uprint("\n" * 3)
            assert expr_tex[i] == s
        else:
            s = py2tex(expr, print_latex=False, print_formula=False)
            assert expr_tex[i] == s


def test_py2tex_py3only(verbose=True, **kwargs):
    """Some tests valid with Python 3 syntax only (Ex: unicodes: ˆ)"""

    if sys.version_info[0] != 3:
        if verbose:
            print("Not Python 3. Ignoring test_py2tex_py3only")
        return

    # Tests
    expr_py = [
        r"k_i__1_i__2ˆj__1ˆj__2",
    ]

    expr_tex = [
        r"$$k_{i_1,i_2}^{j_1,j_2}$$",
    ]

    for i, expr in enumerate(expr_py):
        if verbose:
            uprint("")
            uprint("ˆ")
            uprint("Python formula to convert: {0}".format(expr))
            s = py2tex(expr)
            uprint("Got:")
            b = expr_tex[i] == s
            print(s)
            #            uprint('.. correct =', b)
            if not b:
                uprint("Expected:\n", expr_tex[i])
                uprint("\n" * 3)
            assert b
        else:
            s = py2tex(expr, print_latex=False, print_formula=False)
            assert expr_tex[i] == s


def test_hardcoded_names(verbose=True, **kwargs):
    """Test special numpy functions, greek letters (unicode), and hardcoded
    conventions (ex: eps for \\epsilon)
    """

    # Operators
    assert py2tex("a>2", print_latex=False) == "$$a>2$$"
    assert py2tex("a>=2", print_latex=False) == "$$a>=2$$"
    assert py2tex("3%2", print_latex=False) == "$$3\\bmod2$$"
    assert py2tex("a & b", print_latex=False) == "$$a\\operatorname{and}b$$"
    assert py2tex("a | b", print_latex=False) == "$$a\\operatorname{or}b$$"
    assert py2tex("a ^ b", print_latex=False) == "$$a\\operatorname{xor}b$$"
    assert py2tex("4 << 5", print_latex=False) == "$$4\\operatorname{shiftLeft}5$$"
    assert py2tex("4 >> 5", print_latex=False) == "$$4\\operatorname{shiftRight}5$$"
    assert (
        py2tex("~n == -n - 1", print_latex=False) == "$$\\operatorname{invert}n=-n-1$$"
    )

    # Python syntax
    assert (
        py2tex("sum([k for k in range(1, N)])", print_latex=False)
        == "$$\\sum_{k=1}^{N-1} k$$"
    )
    assert (
        py2tex("sum([k for k in range(1, N+1)])", print_latex=False)
        == "$$\\sum_{k=1}^{N} k$$"
    )
    assert (
        py2tex("sum([k for k in range(1, 11)])", print_latex=False)
        == "$$\\sum_{k=1}^{10} k$$"
    )

    # Math Functions
    assert py2tex("log(x)", print_latex=False) == "$$\\ln\\left(x\\right)$$"
    assert py2tex("np.log10(x)", print_latex=False) == "$$\\log\\left(x\\right)$$"
    assert (
        py2tex("numpy.arccos(x)", print_latex=False) == "$$\\arccos\\left(x\\right)$$"
    )
    # the test below uses unicode symbol, which is valid only in Python2
    if sys.version_info[0] != 3:
        assert (
            py2tex("arcsin(α)", print_latex=False)
            == "$$\\arcsin\\left(\\alpha\\right)$$"
        )
        assert (
            py2tex("arctan(α)", print_latex=False)
            == "$$\\arctan\\left(\\alpha\\right)$$"
        )
    else:
        assert (
            py2tex("arcsin(alpha)", print_latex=False)
            == "$$\\arcsin\\left(\\alpha\\right)$$"
        )
        assert (
            py2tex("arctan(alpha)", print_latex=False)
            == "$$\\arctan\\left(\\alpha\\right)$$"
        )
    assert py2tex("arcsinh(x)", print_latex=False) == "$$\\sinh^{-1}\\left(x\\right)$$"
    assert py2tex("arccosh(x)", print_latex=False) == "$$\\cosh^{-1}\\left(x\\right)$$"

    assert py2tex("np.power(2, 10)", print_latex=False) == "$$2^{10}$$"
    assert py2tex("np.power(ab, c)", print_latex=False) == "$${ab}^c$$"
    assert py2tex("pow(a+b, c)", print_latex=False) == "$$\\left(a+b\\right)^c$$"

    assert (
        py2tex("5*25**2", print_latex=False, tex_multiplier="{\\cdot}")
        == "$$5{\\cdot}{25}^2$$"
    )
    assert py2tex("5*25**2/4", print_latex=False) == "$$\\frac{5\\times{25}^2}{4}$$"

    # Additional function (conventions)
    assert py2tex("kron(i, j)", print_latex=False) == "$$\\delta_{i, j}$$"
    # unknown function:
    assert py2tex("myFunc()") == "$$\\operatorname{myFunc}\\left(\\right)$$"

    # Special characters (conventions):
    assert py2tex("eps*lbd+Lbd", print_latex=False) == "$$\\epsilon \\lambda+\\Lambda$$"


def test_simplify_parser(verbose=True, **kwargs):
    """Test simplifications during Parsing.

    simplify_ints and simplify_fractions implemented by alexhagen
    See PR 7: https://github.com/erwanp/pytexit/pull/7
    """

    # Test simplify_ints:
    assert (
        py2tex("1./5.2", simplify_ints=True, print_latex=False) == "$$\\frac{1}{5.2}$$"
    )
    assert (
        py2tex("1./5.2", simplify_ints=False, print_latex=False)
        == "$$\\frac{1.0}{5.2}$$"
    )

    # Test simplify_fractions:
    assert py2tex("0.5", simplify_fractions=False, print_latex=False) == "$$0.5$$"
    assert (
        py2tex("0.5", simplify_fractions=True, print_latex=False) == "$$\\frac{1}{2}$$"
    )

    # Test simplify_multipliers
    assert py2tex("2*4", print_latex=False) == "$$2\\times4$$"
    assert py2tex("-2*3", print_latex=False) == "$$-2\\times3$$"
    assert py2tex("a*-2", simplify_multipliers=True, print_latex=False) == "$$-2a$$"
    assert (
        py2tex("a*-2", simplify_multipliers=False, print_latex=False)
        == "$$a\\times-2$$"
    )

    # Test simplify_output
    assert py2tex("2e7", simplify_output=True) == "$$2\\times{10}^7$$"
    assert py2tex("2e7", simplify_output=False) == "$$20000000$$"
    assert py2tex("1e7", simplify_output=True) == "$${10}^7$$"
    assert py2tex("1e7", simplify_output=False) == "$$10000000$$"
    assert py2tex("2e-7", simplify_output=True) == "$$2\\times{10}^{-7}$$"
    assert py2tex("2e-7", simplify_output=False) == "$$2e-07$$"
    assert py2tex("1e-7", simplify_output=True) == "$${10}^{-7}$$"
    assert py2tex("1e-7", simplify_output=False) == "$$1e-07$$"


def test_multi():
    """
    sanity check for multi-line input (having import issues with multi2tex, 
    so just pasting the implementation here for now)
    """
    a = "x = 4\ny = 5"
    
    code_arr = a.split('\n')
    tex_arr = [""] * len(code_arr)
    
    for i in range(len(code_arr)):
        tex_arr[i] = py2tex(code_arr[i])
        
    output = '\n'.join(tex_arr)
    
    assert output == "$$x=4$$\n$$y=5$$"


def run_all_tests(verbose=True, **kwargs):

    test_py2tex(verbose=verbose, **kwargs)
    test_py2tex_py3only(verbose=verbose, **kwargs)
    test_hardcoded_names(verbose=verbose, **kwargs)
    test_simplify_parser(verbose=verbose, **kwargs)
    test_multi()


if __name__ == "__main__":
    run_all_tests(verbose=True)
