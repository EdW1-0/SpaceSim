import unittest

from views.orbitViews.orbitViews import (
    OrbitNodeView,
    OrbitLinkView,
    OrbitNodeViewLabel,
    OrbitLinkViewLabel,
    ParticleView,
)

import pygame


class OrbitNodeMock:
    pass


class TestOrbitNodeView(unittest.TestCase):
    def setUp(self):
        self.onm = OrbitNodeMock()
        self.onm.leaf = 0

    def testOrbitNodeView(self):
        self.assertTrue(OrbitNodeView)

    def testOrbitNodeViewConstructor(self):
        self.assertTrue(OrbitNodeView(self.onm))
        self.assertTrue(OrbitNodeView(self.onm, center=(1, 1)))
        self.assertTrue(OrbitNodeView(self.onm, center=(1, 1), selected=True))

    def testOrbitNodeViewAttributes(self):
        onv = OrbitNodeView(self.onm)
        self.assertTrue(hasattr(onv, "rect"))
        self.assertTrue(hasattr(onv, "surf"))
        self.assertTrue(hasattr(onv, "center"))
        self.assertTrue(hasattr(onv, "node"))

    def testOrbitNodeViewCenter(self):
        onm = OrbitNodeMock()
        onm.leaf = 0
        self.assertEqual(OrbitNodeView(onm).center, (0, 0))


class TestOrbitLinkView(unittest.TestCase):
    def setUp(self):
        self.olm = OrbitNodeMock()

    def testOrbitLinkView(self):
        self.assertTrue(OrbitLinkView)

    def testOrbitLinkViewConstructor(self):
        olv = OrbitLinkView(self.olm)
        self.assertTrue(olv)
        self.assertTrue(hasattr(olv, "link"))
        self.assertTrue(hasattr(olv, "surf"))
        self.assertTrue(hasattr(olv, "rect"))

    def testOrbitLinkViewZeroLink(self):
        olv = OrbitLinkView(self.olm)
        rect = olv.rect
        self.assertEqual(rect.width, 0)
        self.assertEqual(rect.height, 10)

    def testOrbitLinkViewHorizontal(self):
        olv = OrbitLinkView(self.olm, (50, 50), (100, 50))
        rect = olv.rect
        self.assertEqual(rect.width, 30)
        self.assertEqual(rect.height, 10)
        self.assertEqual(rect.top, 45)
        self.assertEqual(rect.left, 60)

    def testOrbitLinkViewReverseHorizontal(self):
        olv = OrbitLinkView(self.olm, (50, 50), (10, 50))
        rect = olv.rect
        self.assertEqual(rect.width, 20)
        self.assertEqual(rect.height, 10)
        self.assertEqual(rect.top, 45)
        self.assertEqual(rect.left, 20)

    def testOrbitLinkViewVertical(self):
        olv = OrbitLinkView(self.olm, (50, 50), (50, 100))
        rect = olv.rect
        self.assertEqual(rect.width, 10)
        self.assertEqual(rect.height, 30)
        self.assertEqual(rect.top, 60)
        self.assertEqual(rect.left, 45)

    def testOrbitLinkViewReverseVertical(self):
        olv = OrbitLinkView(self.olm, (50, 100), (50, 10))
        rect = olv.rect
        self.assertEqual(rect.width, 10)
        self.assertEqual(rect.height, 70)
        self.assertEqual(rect.top, 20)
        self.assertEqual(rect.left, 45)


class TestParticleView(unittest.TestCase):
    def testParticleView(self):
        self.assertTrue(ParticleView)

    def testParticleViewConstructor(self):
        pm = OrbitNodeMock()
        self.assertTrue(ParticleView(pm))
        self.assertTrue(hasattr(ParticleView(pm), "particle"))
        self.assertTrue(hasattr(ParticleView(pm), "surf"))
        self.assertTrue(hasattr(ParticleView(pm), "rect"))


class TestOrbitNodeViewLabel(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def testOrbitNodeViewLabel(self):
        self.assertTrue(OrbitNodeViewLabel)

    def testOrbitNodeViewLabelConstructor(self):
        onm = OrbitNodeMock()
        onm.name = "Mars"
        ovl = OrbitNodeViewLabel(onm)
        self.assertTrue(ovl)
        self.assertTrue(hasattr(ovl, "node"))


class TestOrbitLinkViewLabel(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def testOrbitLinkViewLabel(self):
        self.assertTrue(OrbitLinkViewLabel)

    def testOrbitLinkViewLabelConstructor(self):
        onm = OrbitNodeMock()
        onm.deltaV = 26
        ovl = OrbitLinkViewLabel(onm)
        self.assertTrue(ovl)
        self.assertTrue(hasattr(ovl, "link"))
